from .ml.predictor import predict_crop
GUIDANCE={'Rice':'Suitable only where standing water and local varieties are appropriate.','Potato':'Use certified seed and monitor moisture consistently.','Millet':'Consider drought-tolerant local varieties and market access.','Maize':'Split nutrient application based on a soil test.','Pigeon pea':'Use locally recommended varieties and pest monitoring.'}
def recommend(features):
    result=predict_crop(features); result['guidance']=GUIDANCE.get(result['crop'],'Consult local extension services for variety and timing guidance.'); return result
