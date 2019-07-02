app.controller("controller", function($http, $scope, $uibModal, $httpParamSerializer) {

    $scope.get_offset = function(page){
        if (page){
            return (page-1)*10
        }
        return 0
    }
    
    $scope.get_products = function(page) {
        query = {}
        if ($scope.search){
            query.keyword = $scope.search
        }
        const offset = $scope.get_offset(page)
        query.offset = offset
        const param_string = $httpParamSerializer(query)
        $http.get('/products/?' + param_string).success(function(data) {
            $scope.products = data.results
            $scope.meta = { count: data.count, next: data.next, previous: data.previous }
        })
    }

    $scope.change_mode = function(mode) {
        delete $scope.file
        $scope.mode = mode
        if (mode == 1) {
            $scope.get_products()
        }
    }

    $scope.get_host_url = function(){
        return location.hostname+(location.port ? ':'+location.port: '');
    }

    $scope.setup_socket = function(upload_id){
        const url = $scope.get_host_url()
                socket_url = `ws://${url}/ws/messages/${upload_id}/`
                $scope.socket = new WebSocket(socket_url)
                console.log("socket setup")
                $scope.socket.onmessage = function(e) {
                    var data = JSON.parse(e.data);
                    $scope.upload_message = data['message'];
                    $scope.records_saved = data['saved_records'];
                    $scope.upload_status = data['status'];
                    $scope.$apply()
                };
                $scope.socket.onclose = function(e) {
                    console.error('Chat socket closed unexpectedly');
                };
    }

    $scope.get_socket = function(){
        $http.get("/upload-products/").success(function(data){
            if (data.id){
                $scope.setup_socket(data.id)
            }
        })
    }
    
    $scope.initial = function() {
        $scope.get_socket()
        $scope.mode = 1
        $scope.bigCurrentPage=1
        $scope.get_products()
    }

    $scope.download_csv = function(uploadid) {
        window.location.href = '/download-csv/' + String(uploadid) + "/"
    }

    $scope.uploadfile = function() {
        var file = $scope.file[0]
        var extnsn = '.' + file.name.slice((file.name.lastIndexOf(".") - 1 >>> 0) + 2)
        if (['.csv'].indexOf(extnsn) == -1) {
            $scope.invalid_file_error = true
            alert('Invalid file')
            return
        }
        $scope.invalid_file_error = false

        var fd = new FormData();
        //Take the first selected file
        fd.append("file", file);
        $http.post('/upload-products/', fd, {
            withCredentials: true,
            headers: { 'Content-Type': undefined },
            transformRequest: angular.identity
        }).success(function(data) {
            console.log(data)
            $scope.setup_socket(data.upload_id)
            $scope.change_mode(1)
        }).error(function(data, status) {
            if (data.response) {
                alert(data.response)
            } else {
                alert("Invalid file")
            }
        });
    }

    $scope.initial()

    $scope.open = function (product) {
        var modalInstance = $uibModal.open({
          animation: $scope.animationsEnabled,
          ariaLabelledBy: 'modal-title',
          ariaDescribedBy: 'modal-body',
          templateUrl: 'myModalContent.html',
          controller: 'ModalInstanceCtrl',
          controllerAs: '$ctrl',
          resolve: {
            product: function () {
              return product;
            }
          }
        });
    
        modalInstance.result.then(function (selectedItem) {
            $scope.get_products($scope.bigCurrentPage);
        }, function () {
          console.info('Modal dismissed at: ' + new Date());
        });
      };

})

app.controller('ModalInstanceCtrl', function ($uibModalInstance,$http, product) {
    var $ctrl = this;

    $ctrl.product = product

    $ctrl.delete = function(){
        $http.delete(`products/${$ctrl.product.id}`).success(function(data){
            $uibModalInstance.close($ctrl.product);
        })
    }

    $ctrl.ok = function () {
        $http.put(`products/${$ctrl.product.id}`, $ctrl.product).success(function (data) {
            $uibModalInstance.close($ctrl.product);
        })
    };

    $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});