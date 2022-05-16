// For the example - show interactions with the table
var eventFired = function ( type ) {
    // var n = document.querySelector('#demo_info');
    // n.innerHTML += '<div>'+type+' event - '+new Date().getTime()+'</div>';
    // n.scrollTop = n.scrollHeight;     
}
 
document.addEventListener('DOMContentLoaded', function () {
    let table = new DataTable('#example');
 
    table
        .on('order', function () {
            eventFired( 'Order' );
        })
        .on('search', function () {
            eventFired( 'Search' );
        })
        .on('page', function () {
            eventFired( 'Page' );
        });
});