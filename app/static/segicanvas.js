var c = document.getElementById("pixelcanvas");
var ctx = c.getContext("2d");
var pixelCanvasSize = 64;
const pixelSize = 8;
var selectedPixel = [0, 0];
var oldSelectedPixel = [];
var selectedColour = "black"
var drawing = false;
var drawingalt = false;
var canvas_id = null;
var upvoted = false;

const colours = [
    "rgba(0,0,0,0)",
    "rgba(255,255,255,255)",
    "rgba(0,0,0,255)",
    "rgba(255,0,0,255)",
    "rgba(0,255,0,255)",
    "rgba(0,0,255,255)",
    "rgba(255,255,0,255)",
    "rgba(0,255,255,255)",
    "rgba(255,0,255,255)"
];

const colourNames = {
    "white": 1,
    "black": 2,
    "red": 3,
    "green": 4,
    "blue": 5,
    "yellow": 6,
    "turquoise": 7,
    "purple": 8,

};


//drawPixel(4,4,0,0,0) - draws a black pixel at 4,4
function drawPixel(x, y, colour) {
    ctx.fillStyle = colours[colourNames[colour]];
    ctx.fillRect(x*pixelSize, y*pixelSize, pixelSize, pixelSize);
}

// canvasToString() and parseCanvasString(canvasstring) - handles saving and loading canvas to and from a string of numbers
function canvasToString() {
    var finalstring = ""
    for(i=0;i<pixelCanvasSize;i++){
        for (j=0;j<pixelCanvasSize;j++) {
            var temp = ctx.getImageData(j*pixelSize,i*pixelSize,1,1).data;
            finalstring += (colours.indexOf("rgba("+temp[0]+","+temp[1]+","+temp[2]+","+temp[3]+")")).toString();
        }
    }
    return finalstring
}

function parseCanvasString(canvasstring) {
    for (i=0;i<pixelCanvasSize;i++) {
        for (j=0;j<pixelCanvasSize;j++) {
            ctx.fillStyle = colours[canvasstring.charAt((pixelCanvasSize*i)+j)];
            if (canvasstring.charAt((pixelCanvasSize*i)+j) == '0') {
                ctx.fillStyle = colours[colourNames["white"]]
            } 
            ctx.fillRect(j*pixelSize, i*pixelSize, pixelSize, pixelSize);
        }
    }
}

// Mouse Functionality ----------------------------------------------------

c.addEventListener("mousemove", function(e) {
    selectedPixel = [Math.floor(e.offsetX/pixelSize), Math.floor(e.offsetY/pixelSize)];
    if (drawing) {
        drawPixel(selectedPixel[0], selectedPixel[1], selectedColour);
        socket.emit("pixel", {
            "xpos": selectedPixel[0], 
            "ypos": selectedPixel[1],
            "colour": selectedColour,
            "room": $("#canvasid").html()
        });
    } else
    if (drawingalt) {
        drawPixel(selectedPixel[0], selectedPixel[1], "white");
        socket.emit("pixel", {
            "xpos": selectedPixel[0], 
            "ypos": selectedPixel[1],
            "colour": "white",
            "room": $("#canvasid").html()
        });
    }
});

c.addEventListener("mousedown", function(e){
    if (e.button == 0) {
        drawPixel(selectedPixel[0], selectedPixel[1], selectedColour);
        socket.emit("pixel", {
            "xpos": selectedPixel[0], 
            "ypos": selectedPixel[1],
            "colour": selectedColour,
            "room": $("#canvasid").html()
        });
        drawing = true;
    } else if (e.button == 2) {
        console.log("right button");
        drawPixel(selectedPixel[0], selectedPixel[1], "white");
        socket.emit("pixel", {
            "xpos": selectedPixel[0], 
            "ypos": selectedPixel[1],
            "colour": "white",
            "room": $("#canvasid").html()
        });
        drawingalt = true;
    }
});


c.addEventListener("mouseup", function(e){
    drawing = false;
    drawingalt = false;
    socket.emit("save", {
        "id": $("#canvasid").html(),
        "canvasstring": canvasToString()
    });
});

function selectColour(colour) {
    var colourBoxes = document.getElementsByClassName("box");
    var n = colourBoxes.length;
    for (i=0;i<n;i++) {
        var e = colourBoxes[i];
        e.classList.remove("selected");
    }
    document.getElementsByClassName(colour)[0].classList.add("selected");
    selectedColour = colour;
}


// Socket.IO functionality ------- Real-Time pixel-placing & synchronisation

socket.on("pixel", function(data) {
    //console.log(data);
    drawPixel(data.xpos, data.ypos, data.colour);
});

socket.on("test", function(data) {
    console.log("SEGI by enducube");
});

function upvote() {
    socket.emit("upvote", {
        "id": $("#canvasid").html()
    });
}



