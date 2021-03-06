
from flask import jsonify, Blueprint, request

from flask_restful import Resource, Api
from services.cost_prediction_model.cost_prediction_model import CostPredictionModel
from services.building_vol_calculator.building_vol_metres_calculator import BuildingVolMetresCalculator
from measurement.utils import guess

from services.error_handling.exceptions.cost_prediction_failed import CostPredictionFailed


class FitOutCostPrediction(Resource):
    def post(self):
        try:
            costPredictionParameters = request.get_json()

            buildingVolumeCalculator = BuildingVolMetresCalculator(costPredictionParameters['floorArea'], costPredictionParameters['averageFloorHeight'])
            buildingVolumeValue = buildingVolumeCalculator.calculateVolume()

            isCatAIncluded = 0
            isCatBIncluded = 0
            isCatAAndBIncluded = 0

            if costPredictionParameters['isCatAIncluded'] == True and costPredictionParameters['isCatBIncluded'] == True:
                isCatAAndBIncluded = 1
            elif costPredictionParameters['isCatAIncluded'] == True and costPredictionParameters['isCatBIncluded'] == False:
                isCatAIncluded = 1
            elif costPredictionParameters['isCatAIncluded'] == False and costPredictionParameters['isCatBIncluded'] == True:
                isCatBIncluded = 1

            costPredictionParametersForModel = [
                buildingVolumeValue, isCatAIncluded, isCatBIncluded, isCatAAndBIncluded]

            costPredictionModel = CostPredictionModel()
            cost = costPredictionModel.predictCost(
                costPredictionParametersForModel)

        except ValueError as error:
            raise CostPredictionFailed(error.args[0], response_status_code=500)

        except TypeError as error:
            raise CostPredictionFailed(error.args[0], response_status_code=500)

        except KeyError as error:
            raise CostPredictionFailed(error.args[0], response_status_code=500)

        # return a json value
        return jsonify({'cost': cost})


fitout_cost_prediction_api = Blueprint(
    'resources.fit_out_cost_prediction', __name__)

api = Api(fitout_cost_prediction_api)
api.add_resource(
    FitOutCostPrediction,
    '/fitOutCostPrediction',
    endpoint='fitOutCostPrediction'
)
