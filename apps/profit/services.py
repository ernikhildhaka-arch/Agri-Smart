def calculate(data):
    costs=sum(data[x] for x in ('seed_cost','fertilizer_cost','pesticide_cost','labour_cost','irrigation_cost','other_cost')); revenue=data['yield_amount']*data['market_price']; profit=revenue-costs
    return {'total_cost':costs,'revenue':revenue,'profit':profit,'per_area':profit/data['land_area'],'cost_parts':[(k.replace('_',' ').title(),data[k]) for k in ('seed_cost','fertilizer_cost','pesticide_cost','labour_cost','irrigation_cost','other_cost')]}
