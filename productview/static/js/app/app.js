var app = angular.module('productViewApp', ["ngCookies","ui.bootstrap"])

app.config(function($interpolateProvider) {
 $interpolateProvider.startSymbol('{[{');
 $interpolateProvider.endSymbol('}]}');
 //$resourceProvider.defaults.stripTrailingSlashes = false;
});


app.run([
 '$http',
 '$cookies',
 function($http, $cookies) {
 $http.defaults.headers.post['X-CSRFToken'] =   $cookies.get('csrftoken');
 }
]);

app.run(['$rootScope','$http', function($rootScope,$http) {
  
}]);

app.directive("selectNgFiles", function() {
  return {
    require: "ngModel",
    link: function postLink(scope,elem,attrs,ngModel) {
      elem.on("change", function(e) {
        var files = elem[0].files;
        ngModel.$setViewValue(files);
      })
    }
  }
})