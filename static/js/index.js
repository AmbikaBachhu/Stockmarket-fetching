nifty_scrapper_app.controller('index_controller',['$scope','$timeout','$http',
    function($scope,$timeout,$http)
    {
        $scope.init = function(gainer_data, loser_data)
        {
            $scope.gainer_data = gainer_data
            $scope.loser_data = loser_data
        }


        $scope.get_nifty_data = function()
        {

            var req = {
                method: 'GET',
                url: '/get_nifty_data',
                headers: {
                    'Content-Type': false
                },
                data: ''
            }
            $http(req).then(function successCallback(response) {
                if(response.data.response == 'success')
                {
                    $scope.gainer_data = response.data.response_nifty.gainer_json
                    $scope.loser_data = response.data.response_nifty.loser_json
                }
            }, function errorCallback(response) {
                console.log('Failure');

            });
        }

        setInterval(function(){
              $scope.get_nifty_data();
            }, 3)
    }])