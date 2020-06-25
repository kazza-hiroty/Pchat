document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let room = "Lounge";
    joinRoom("Lounge");

    //Display incoming 
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.username){
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg+ br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);

        }else{
            printSysMsg(data.msg);
        }
    }); 

    //Send message
    document.querySelector('#send_message').onclick = () =>{
        socket.send({'msg': document.querySelector('#user_message').value, 'username': username, 'room':room });

        //clear input area
        document.querySelector('#user_message').value = '';
    };

    //Room selection
    document.querySelectorAll('.select-room').forEach(p =>{
        p.onclick = () =>{
            let newRoom = p.innerHTML;
            if(newRoom == room){ //if the person is already in room, send the notification
                msg=`You are already in ${room} room.`;
                printSysMsg(msg);  //using method to send notification
            }else{  //if the persoin is not already in the selected room, leave the current room and join the new room 
                leaveRoom(room);  //function to leave the room
                joinRoom(newRoom);
                room = newRoom; 
            }
        }
    })

    function leaveRoom(room){
        socket.emit('leave',{'username' : username, 'room': room});
    }
    //join room 
    function joinRoom(room){
        socket.emit('join',{'username':username, 'room': room});
        //clear text box
        document.querySelector('#display-message-section').innerHTML = '';

        //autofocus on textbox
        document.querySelector('#user_message').focus();
    }

    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML =msg;
        document.querySelector('#display-message-section').append(p);
    }


    


})