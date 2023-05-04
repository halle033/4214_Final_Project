from app import app

##### FORMAT PERCENTAGE #####
@app.template_filter()
def percentageFormat(value):
    value = float(value)
    return f"{value:,.2f}%"

@app.template_filter()
def numberFormat(value):
    value = float(value)
    return f"{value:,.2f}"


##### FORMAT CURRENCY #####
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return f"${value:,.2f}"

##### FORMAT QUANTITY #####
@app.template_filter()
def quantityFormat(value):
    value = float(value)
    return f"{value:,.6f}"


##### FORMAT DATE #####
@app.template_filter()
def dateFormat(value):
    return value.strftime("%Y-%m-%d")]]]]][[[[[[[[[[[[]]]]]]]]]]]]