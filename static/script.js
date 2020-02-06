// then page is loaded
document.addEventListener("DOMContentLoaded", () => {

    // connect to web socket 
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

    // when connected, configure buttons
    socket.on('connect', () => {

        // configure Create channel button
        createChannelBtn = document.querySelector(".input-group-prepend");
        createChannelBtn.onclick = () => {
            // take new channel name from input field
            const newChannelName = document.querySelector(".search").value;
            socket.emit("create channel", { "name": newChannelName });

        };

        // configure Send button
        sendMessageBtn = document.querySelector(".input-group-append");
        sendMessageBtn.onclick = () => {
            //take message
            const text = document.querySelector(".type_msg").value;
            socket.emit("send message", { "text": text })
        };

    });

    // create channel
    socket.on("channel created", data => {
        // get channel list 
        const channelList = document.querySelector(".contacts");
        // add new channel to the list
        channelList.innerHTML = channelList.innerHTML + data;
    });

    // in case of error
    socket.on("error", data => {
        alert(data);
    });

    return false;
});