function checkMongoConnection(){
    // This function test the connection to Mongo DB
          $.ajax({
                    url: '/check/mongo/connect',
                    success: function(response){
                        if(response.success){
                            $('#testlog').append('Ok. Mongo DB is working... <br />');
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
                            msg = 'Get random item \'no\':' +  response.item.no + ' for time <b>' + response.time + 's</b><br />'
                            $('#testlog').append(msg);
                        }
                        else{
                            //$('#error_log').html('Can\'t connect to Mongo DB');
                        }
                        
                    }
                })
}

// ==============================================================
// Main test function is here
function startTest(){
    checkMongoConnection();
    $('#testlog').append('Let\' start the test <br />');
    createDocs(5);
    getRandomItem();
    dropCollection();
    
    $('#testlog').append('<div style="padding: 10px; background-color: #b5eab8; font-weight: bold;">Test is ended</div>');
}
