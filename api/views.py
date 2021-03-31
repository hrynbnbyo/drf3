from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book
from api.serializer import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            book_serializer = BookModelSerializer(book_obj).data
            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_serializer
            })
        else:
            book_set = Book.objects.all()
            book_set_serializer = BookModelSerializer(book_set, many=True).data
            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_set_serializer
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = BookDeModelSerializer(data=request_data)
        # 检验是否合法
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status": 201,
            "message": "创建成功",
            "results": BookModelSerializer(book_obj).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            a = [book_id]
        # 判断要删除的图书是否存在 且还未删除
        response = Book.objects.filter(pk__in=a, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })

        return Response({
            "status": 400,
            "message": "删除失败"
        })
    
    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "要更新图书不存在"
            })
        # request_data: 要修改的数据
        book_serializer = BookModelSerializer(data=request_data, instance=book_obj)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookModelSerializer(book).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })
        # 如果要修改部分字段，只需要指定参数partial=True即可
        book_serializer = BookModelSerializer(data=request_data, instance=book_obj, partial=True)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookModelSerializer(book).data
        })


class BookAPIViewV2(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            book_serializer = BookModelSerializerV2(book_obj).data

            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_serializer
            })
        else:
            book_set = Book.objects.all()
            book_set_serializer = BookModelSerializerV2(book_set, many=True).data
            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_set_serializer
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        # 判断增一个还是增多个
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "请求参数格式有误"
            })

        serializer = BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 201,
            "message": "创建成功",
            "results": BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            a = [book_id]
        # 判断要删除的图书是否存在是否已经删除
        response = Book.objects.filter(pk__in=a, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })

        return Response({
            "status": 400,
            "message": "删除失败或删除的图书不存在"
        })

    def put(self, request, *args, **kwargs):
        # 要修改的值
        request_data = request.data
        # 图书id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookModelSerializerV2(book).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })

        # 如果要修改部分字段，只需要指定参数partial=True即可
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_serializer.is_valid(raise_exception=True)

        book = book_serializer.save()

        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookModelSerializerV2(book).data
        })
