
var app = angular.module('app', ["ngResource","chart.js","ngMaterial"]);

app.controller('controller', function controller($scope,$http) {
   $scope.Title="Web İndeksleme Uygulaması";
   $scope.soru=0;

   /*$scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
   //$scope.series = ['Series A']; 
   $scope.data = [
     [65, 59, 80, 81, 56, 55, 40]
   ];*/

   $scope.s1incele=function(){    
    $http({
        method: "POST",
        url: "http://127.0.0.1:5000/s1",
        data: {"url":$scope.url},
        headers:{ 
          "Content-Type":"application/json;",
          'Access-Control-Allow-Origin': '*',
          "Access-Control-Allow-Headers": "X-PINGOTHER,Content-Type",          
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
        }     
    }).then(function success(response) {
      $scope.labels=[];
      $scope.data=[];
        for(var keyName in response.data){        
            $scope.labels.push(keyName);
            $scope.data.push(response.data[keyName]);
        }
    })};


    $scope.s2incele=function(){    
      $http({
          method: "POST",
          url: "http://127.0.0.1:5000/s2",
          data: {"url":$scope.url},
          headers:{ 
            "Content-Type":"application/json;",
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Headers": "X-PINGOTHER,Content-Type",          
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
          }     
      }).then(function success(response) {
        $scope.labelS2=[];
        $scope.dataS2=[];
          for(var keyName in response.data){        
              $scope.labelS2.push(keyName);
              $scope.dataS2.push(response.data[keyName]);
          }
    })};


    $scope.s3karsilastir=function(){    
        $http({
            method: "POST",
            url: "http://127.0.0.1:5000/s3",
            data: {"url":$scope.url,
                   "url2":$scope.url2},
            headers:{ 
              "Content-Type":"application/json;",
              'Access-Control-Allow-Origin': '*',
              "Access-Control-Allow-Headers": "X-PINGOTHER,Content-Type",          
              "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
            }     
        }).then(function success(response) {
          $scope.labelS3a=[];
          $scope.dataS3a=[];
          $scope.labelS3b=[];
          $scope.dataS3b=[];   
          $scope.labelS3c=[];
          $scope.dataS3c=[];  
            url1 = angular.fromJson(response.data["url1"]);
            for(var keyName in url1){        
                $scope.labelS3a.push(keyName);
                $scope.dataS3a.push(url1[keyName]);
            }
            url2 = angular.fromJson(response.data["url2"])
            for(var keyName in url2){        
              $scope.labelS3b.push(keyName);
              $scope.dataS3b.push(url2[keyName]);
            }

            kesisim = angular.fromJson(response.data["kesisim"]);
            for(var keyName in kesisim){        
              $scope.labelS3c.push(keyName);
              $scope.dataS3c.push(kesisim[keyName]);
            }
            
            $scope.skor =  response.data["skor"];            

    })};

    $scope.Urls=[];

    $scope.urlEkle = function (url){
      const index = $scope.Urls.indexOf(url);
      if (index == -1) {
        $scope.Urls.push(url)
      }          
    };

    $scope.Sil = function (url){
      const index = $scope.Urls.indexOf(url);
      if (index > -1) {
        $scope.Urls.splice(index, 1);
      }
    };

    

    $scope.s4karsilastir=function(){   
      $scope.progress=true; 
      $http({
          method: "POST",
          url: "http://127.0.0.1:5000/s4",
          data: {"url":$scope.url,
                 "urls":$scope.Urls},
          headers:{ 
            "Content-Type":"application/json;",
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Headers": "X-PINGOTHER,Content-Type",          
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
          }     
      }).then(function success(response) { 
        $scope.s4Skor=angular.fromJson(response.data);
        $scope.progress=false;    
    })};


    $scope.GrafikGoster = function (data){
      data = angular.fromJson(data)
      console.log(data);
      $scope.labelS4=[];
      $scope.dataS4=[];
      for(var keyName in data){    
        console.log(keyName);
        console.log(data[keyName]);     
        $scope.labelS4.push(keyName);
        $scope.dataS4.push(data[keyName]);
      }
    };



    $scope.s5analiz=function(){    
      $scope.progress=true;
      $http({
          method: "POST",
          url: "http://127.0.0.1:5000/s5",
          data: {"url":$scope.url,
                 "urls":$scope.Urls},
          headers:{ 
            "Content-Type":"application/json;",
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Headers": "X-PINGOTHER,Content-Type",          
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
          }     
      }).then(function success(response) { 
        $scope.labelS5=[];
        $scope.dataS5=[];
        $scope.s4Skor=angular.fromJson(response.data["data"]);  
        
        $scope.alakali=angular.fromJson(response.data["alakali"]);  
        console.log($scope.alakali)
        $scope.progress=false;
    })};

  });
