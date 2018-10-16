var permissionApp = angular.module('permissionApp', []);

permissionApp.controller('SelectUser', ['$scope', function($scope) {

    $scope.users = {};

    $scope.change = function(id) {
        button = $("#usrbtn-" + id);
        if(!$scope.clicked(id)) {
            button.addClass('active');
        } else {
            button.removeClass('active');
        }
    }

    $scope.clicked = function(id) {
        if ($scope.users[id]) {
            return true;
        }
        return false;
    };
}]);

permissionApp.controller('EditUser', ['$scope', '$http', function($scope, $http) {

    $scope.perm = {};
    $scope.user = {};
    $scope.submit = {};

    $scope.init = function(user) {
        $scope.user = user;
        $scope.cancel();                
    };

    $scope.submit = function() {
        var data = $.extend({id: $scope.user.id}, $scope.perm);

        $http.post('/users/privileges/set', data, {headers: {'X-CSRFToken': csrf_token}}).then(
            function(response) {
                // success

                if(response.data == 'true') {

                    $scope.submit.success = true;
                    $scope.submit.fail = false;

                    $scope.user.add_user = $scope.perm.add_user;
                    $scope.user.change_perm = $scope.perm.change_perm;
                    $scope.user.change_settings = $scope.perm.change_settings;
                    $scope.user.reboot = $scope.perm.reboot;
                } else {
                    $scope.submit.fail = true;
                    $scope.submit.success = false;
                }
            }, function(response) {
                $scope.submit.fail = true;
                $scope.submit.success = false;
                // fail
            }
        )
    };

    $scope.cancel = function() {
        $scope.submit.fail = false;
        $scope.submit.success = false;


        $scope.perm.add_user = $scope.user.add_user;
        $scope.perm.change_perm = $scope.user.change_perm;
        $scope.perm.change_settings = $scope.user.change_settings;
        $scope.perm.reboot = $scope.user.reboot;
    };

    $scope.update = function() {
        $scope.submit.fail = false;
        $scope.submit.success = false;
    }
}]);