var map;
var marker;

function map(){
    var mapContainer = document.getElementById('map'); // 지도를 표시할 div 
    var myLat = document.getElementById('myLat').value;
    var myLong = document.getElementById('myLong').value;
    
    mapOption = { 
        center: new kakao.maps.LatLng(myLat, myLong), // 지도의 중심좌표
        level: 8 // 지도의 확대 레벨
    };

    map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다   
}

function makeMarker(lat, long){
    // 마커가 표시될 위치입니다 
    var markerPosition  = new kakao.maps.LatLng(lat, long); 

/*    
    var mapContainer = document.getElementById('map'); // 지도를 표시할 div 
    mapOption = { 
        center: markerPosition, // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

    map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
*/
    // 마커를 생성합니다
    marker = new kakao.maps.Marker({
        position: markerPosition
    });

    // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);
}

function removeMarker(){
    marker.setMap(null);  
}