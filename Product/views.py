from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Product, ProductVariant, ProductCombination, Category
from django.db.models import Q
import nltk
from nltk.corpus import stopwords
from django.core.paginator import Paginator
from django.db.models import Count

STOPWORDS = set(stopwords.words('english'))
STOPWORDS_ru = set(stopwords.words('russian'))
STOPWORDS_tj = set(stopwords.words('tajik'))


def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    product_variants = ProductVariant.objects.filter(product=product)
    distinct_combinations = ProductCombination.objects.filter(
        product_v__product=product
    ).distinct()
    # Calculate size counts based on the distinct combinations
    size_counts = distinct_combinations.values('size__name').annotate(
        product_count=Count('product_v')
    )
    color_counts = distinct_combinations.values(
        'color__name', 'color__code').annotate(
        product_count=Count('product_v'))

    context = {
        'product': product,
        'size_counts': size_counts,
        'color_counts': color_counts,
        'product_variants': product_variants,
    }
    return render(request, 'Product/detail.html', context)


class ProductList(ListView):
    model = Product
    template_name = 'Product/product_list_view.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(product_status='published')

        search_query = self.request.GET.get('title')
        if search_query:
            # Tokenize search query and remove stopwords
            tokens = nltk.word_tokenize(search_query.lower())
            tokens = [token for token in tokens if token not in STOPWORDS]
            # Construct Q objects to search for similar titles and descriptions
            title_q = Q(title__icontains=search_query)
            desc_q = Q()
            for token in tokens:
                desc_q &= Q(description__icontains=token)
            # Combine title and description queries using OR
            queryset = queryset.filter(title_q | desc_q)

        # sort by
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'popularity':
            queryset = queryset.filter(featured=True)

        # price, color, size

        selected_price_ranges = self.request.GET.getlist('prices')
        if selected_price_ranges:
            if 'all' in selected_price_ranges:
                pass
            else:
                for i in selected_price_ranges:
                    price_start = int((i.split(','))[0])
                    price_end = int((i.split(','))[1]) - 0.01
                    queryset = queryset.filter(price__range=(price_start, price_end))

        selected_colors = self.request.GET.getlist('colors')
        if selected_colors:
            if 'all' in selected_colors:
                pass
            else:
                # Filter products by selected color combinations
                color_combinations = ProductCombination.objects.filter(
                    color__id__in=selected_colors
                ).values('product_v__product__id')
                queryset = queryset.filter(id__in=color_combinations)
        selected_sizes = self.request.GET.getlist('sizes')
        if selected_sizes:
            if 'all' in selected_sizes:
                pass
            else:
                size_combinations = ProductCombination.objects.filter(
                    size__name__in=selected_sizes
                ).values('product_v__product__id')
                queryset = queryset.filter(id__in=size_combinations)

        selected_cats = self.request.GET.getlist('cats')
        if selected_cats:
            if 'all' in selected_cats:
                pass
            else:
                queryset = queryset.filter(category__title__in=selected_cats)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_size = int(self.request.GET.get('page_size', 24))
        self.paginate_by = page_size  # Update the pagination property
        products = self.get_queryset()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['movies'] = page_obj
        context['paginator'] = page_obj.paginator
        context['page_obj'] = page_obj
        context['movies_per_page'] = page_size
        # add search and filter values to context
        # Retrieve the scroll position from the query parameter
        scroll_position = self.request.GET.get('scroll')
        context['scroll_position'] = scroll_position
        context['search_name'] = self.request.GET.get('title', '')
        # add sort by
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['origin'] = self.request.GET.get('origin', '')
        # get price range
        # Count the number of products in each price range
        price_diff = 100
        price_counts = []
        queryset = self.get_queryset()  # Use the filtered queryset from get_queryset method
        total_price = 0
        for i in range(4):
            price_start = i * price_diff
            price_end = price_start + ((i + 1) * price_diff)
            count = queryset.filter(price__range=(price_start, price_end-0.01)).count()
            total_price += count
            price_counts.append(count)
        price_bigger400 = queryset.filter(price__gt=400).count()
        context['price_counts'] = price_counts
        context['price_bigger400'] = price_bigger400
        context['total_price_count'] = total_price+price_bigger400

        color_counts = ProductCombination.objects.filter(product_v__product_status='published').values(
            'color_id', 'color__code').annotate(
            product_count=Count('product_v__product'))
        color_total = 0
        for i in color_counts:
            color_total += i["product_count"]
        context['color_total'] = color_total
        context['color_counts'] = color_counts

        filtered_products = self.get_queryset()
        # distinct_products = Product.objects.filter(product__in=filtered_products).distinct()
        # category_counts = filtered_products.objects.values(
        #     'category__title').annotate(
        #     product_count=Count('product_v__product'))
        # category_total = 0
        # for s in category_counts:
        #     category_total += s["product_count"]
        # context['category_total'] = category_total
        # context['category_counts'] = category_counts

        distinct_categories = Category.objects.filter(product__in=filtered_products).distinct()

        # Annotate each category with the count of products in that category within the filtered queryset
        distinct_categories = distinct_categories.annotate(product_count=Count('product'))
        print(distinct_categories)
        # Add the distinct_categories queryset to the context
        context['category_counts'] = distinct_categories

        # Get distinct ProductCombination instances related to the filtered products
        distinct_combinations = ProductCombination.objects.filter(
            product_v__product__in=filtered_products
        ).distinct()
        # Calculate size counts based on the distinct combinations
        size_counts = distinct_combinations.values('size__name').annotate(
            product_count=Count('product_v__product')
        )
        size_total = 0
        for size_count in size_counts:
            size_total += size_count["product_count"]
        context['size_total'] = size_total
        context['size_counts'] = size_counts

        context['selected_colors'] = self.request.GET.getlist('colors')
        context['selected_price_ranges'] = self.request.GET.getlist('prices')
        context["selected_sizes"] = self.request.GET.getlist('sizes')
        context["selected_categories"] = self.request.GET.getlist('cats')

        return context









