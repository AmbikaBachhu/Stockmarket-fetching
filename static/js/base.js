var nifty_scrapper_app = angular.module('nifty_scrapper', [])
nifty_scrapper_app.controller('base_controller',['$scope','$timeout','$http',
    function($scope,$timeout,$http)
    {
        $scope.init = function()
        {
        }
    }])

nifty_scrapper_app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
