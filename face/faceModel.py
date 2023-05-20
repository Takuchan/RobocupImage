class faceAllDataModel:
    count = 0
    def __init__(self):
        faceAllDataModel.count += 1
    def set_value(self,list_data):
        self.list_data = list_data


class singlePointFaceModel:
    def set_single_point(self,facePointNumber,x_p,y_p):
        self.facePointNumbe = facePointNumber
        self.x = x_p
        self.y = y_p