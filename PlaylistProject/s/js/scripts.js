var displayShows = angular.module("displayShows", []);

displayShows.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
});

displayShows.factory("Shows", function ($http) {

    var openShowsAPI = {};

    openShowsAPI.getShows = function () {
        return $http({
            method: "JSON",
            url: "./data"
        });
    };

    return openShowsAPI;

});

function showsCtrl($scope, Shows) {
    Shows.getShows().success(function (response) {
        $scope.shows = response.shows;
    });

}