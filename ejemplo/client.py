import grpc
import route_guide_pb2
import route_guide_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')
stub = route_guide_pb2_grpc.RouteGuideStub(channel)

feature = stub.GetFeature(point)
