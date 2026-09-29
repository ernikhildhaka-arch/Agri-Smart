def analyse(data):
    nutrients={name: 'Low' if data[name]<30 else 'Adequate' if data[name]<70 else 'High' for name in ('nitrogen','phosphorus','potassium')}
    condition='Acidic' if data['ph']<6.0 else 'Alkaline' if data['ph']>7.8 else 'Near neutral'
    missing=', '.join(k.title() for k,v in nutrients.items() if v=='Low') or 'No obvious deficiency from these inputs'
    irrigation='Irrigate cautiously; moisture is already high.' if data['moisture']>60 else 'Check field moisture regularly and irrigate according to crop stage.'
    return {'condition':condition,'nutrients':nutrients,'fertilizer':f'Consider a soil-test-guided plan. Attention: {missing}.','irrigation':irrigation}
