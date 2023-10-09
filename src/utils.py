def sort_alpha_digit(item):
    # sort alphabetically first, numerically second
    return (item[0].isdigit(), item)

# 
def get_sorted_sizes(sales_data):
    # sort sizes first by letter then by digit
    # eg. first "XXL", then "3XL"
    return sorted(sales_data['Size'].unique().tolist(), key=sort_alpha_digit)
