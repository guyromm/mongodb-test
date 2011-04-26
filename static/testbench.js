var getMarkerTimeArr = Array();
var itemCountArr = Array();
var getRandomTimeArr = Array();
var mongoAlive = false;

function checkMongoConnection(){
    // This function test the connection to Mongo DB
          $.ajax({
                    url: '/check/mongo/connect',
                    success: function(response){
                        if(response.success){
                            $('#testlog').append('Ok. Mongo DB is working... <br />');
                            mongoAlive = true;
                        }
                        else{
                            $('#error_log').html('Can\'t connect to Mongo DB');
                        }
                        
                    }
                })
}
        
function createDocs(amount){
            // This function tells server to create 'amount' amount of random docs
            $.ajax({
                    url: '/create/docs/' + amount,
                    success: function(response){
                        if(response.success){
                            msg = 'Create ' + amount + ' docs in Mongo DB. Time is <b>' + response.time + 's</b><br />'
                            $('#testlog').append(msg);
                        }
                        else{
                            //$('#error_log').html('Can\'t connect to Mongo DB');
                        }
                        
                    }
                })
}

function dropCollection(){
        $.ajax({
                    url: '/drop/collection' ,
                    success: function(response){
                        if(response.success){
                            msg = 'Test collection was dropped for time <b>' + response.time + 's</b><br />';
                            $('#testlog').append(msg);
                        }
                        else{
                            //$('#error_log').html('Can\'t connect to Mongo DB');
                        }
                        
                    }
                })
    }
    
function getRandomItem(){
        $.ajax({
                    url: '/get/random' ,
                    success: function(response){
                        if(response.success){
                            getRandomTimeArr.push(response.time);
                            msg = 'Get random item \'no\':' +  response.item.no + ' for time <b>' + response.time + 's</b><br />'
                            $('#testlog').append(msg);
                        }
                    }
                })
}

function insert_marker(marker_id){
        $.ajax({
                url: '/insert/marker/' + marker_id,
                 success: function(response){
                     if(response.success){
                            //alert('all right');
                     }
                 }
              })
}

function get_count(i){
        $.ajax({
                url: '/get/count',
                success: function(response){
                    if(response.success){
                        itemCountArr.push(response.count);
                        msg = 'Current count of items in collection is <span style="color: #800000;">' + response.count + '</span><br />';
                        $('#testlog').append(msg);
                                                    
                        }
                    }
                })
    
}

function get_marker(marker_id){
        $.ajax({
                url: '/get/marker/' + marker_id,
                 success: function(response){
                     if(response.success){
                         getMarkerTimeArr.push(response.time);
                         msg = 'Get marker #' + marker_id + '. Time is <b>' + response.time + '</b><br />';
                         $('#testlog').append(msg);   
                     }
                 }
              })
    }

// ==============================================================
// Main test function is here
function startTest(){
    checkMongoConnection();
    if (!mongoAlive){ return };
    
    $('#testlog').append('Let\' start the test <br />');
    for (i = 0; i < 100; i++){
        insert_marker(i);
        createDocs(10000);
        get_count();
        getRandomItem();
        get_marker(i)
        
        break;
    }
    
    dropCollection();   
    
    $('#testlog').append('<div style="padding: 10px; background-color: #b5eab8; font-weight: bold;">Test is ended</div>');
}
