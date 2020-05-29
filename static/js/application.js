$(document).ready(function () {
    const input = document.querySelector('input');

    input.addEventListener('change', updateValue);

    function updateValue(e) {
        console.log(e.target.value);
    }
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    //receive details from server
    socket.on('newnumber', function (msg) {
        bid = '<p>' + msg.bid + '</p>';
        ask = '<p>' + msg.ask + '</p>';
        vol = '<p>' + msg.vol + '</p>';
        $('#bid').html(bid);
        $('#ask').html(ask);
        $('#vol').html(vol);
    });
    
   
});