 function findWalls(map){
        baseMap = [];
        subMap = [];
        for (i = 0; i < map.length; i++) {
            baseMap[i] = [];
            subMap[i] = [];
            for (j = 0; j < map[0].length; j++) {
                baseMap[i][j] = baseQuad(map[i][j]);
                subMap[i][j] = [];
            }
        }
        for (i = 0; i <= map.length; i++) {
            for (j = 0; j <= map[0].length; j++) {
                subQuad(i, j);
            }
        }

        return subMap;

        function baseQuad(tile) {
            //Translate tile into base subtiles.
            var blank = [0, 0, 0, 0],
                solid = [1, 1, 1, 1],
                diagonal = [3, 0, 4, 2];
            if (tile == "1")
                return solid;
            //If the tile is a diagonal tile, rotate it into the correct tile by shifting the diagonal array.
            else if (Math.floor(tile) == "1") {
                for (offset = Number((tile + "").substr(-1)) - 1; offset > 0; offset--)
                    diagonal.unshift(diagonal.pop());
                return diagonal;
            }
            else
                return blank;
        }

        function getQuad(x, y) {
            //Get the base tiles offset 1 subtile to the left and 1 up.
            quadArray = [0,0,0,0];
            if (baseMap[x]) {
                if (baseMap[x][y])
                    quadArray[0] = baseMap[x][y][0];
                if (baseMap[x][y-1])
                    quadArray[3] = baseMap[x][y - 1][3];
            }
            if (baseMap[x - 1]) {
                if (baseMap[x - 1][y])
                    quadArray[1] = baseMap[x - 1][y][1];
                if (baseMap[x - 1][y - 1])
                    quadArray[2] = baseMap[x - 1][y - 1][2];
            }
            return quadArray;
        }

        function setQuad(x, y, quad) {
            //Set subtiles offset 1 subtile to the left and 1 up.
            if (subMap[x]) {
                if (subMap[x][y])
                    subMap[x][y][0] = quad[0];
                if (subMap[x][y - 1])
                    subMap[x][y - 1][3] = quad[3];
            }
            if (subMap[x - 1]) {
                if (subMap[x - 1][y])
                    subMap[x - 1][y][1] = quad[1];
                if (subMap[x - 1][y - 1])
                    subMap[x - 1][y - 1][2] = quad[2];
            }
        }

        function subQuad(x, y) {
            var quad = getQuad(x, y),
                angle = 0,
                angles = [],
            //If the start tile connects with the end tile, the angle starts as open.
                openAngle = (quad[3] == 1 || quad[3] == 2 || quad[3] == 3) && (quad[0] == 1 || quad[0] == 2 || quad[0] == 4),
                offset = openAngle;

            //If the tile is blank, return a blank tile.
            if (quad[0] + quad[1] + quad[2] + quad[3] == 0)
                return setQuad(x, y, quad);

            //If the tile is solid check if any of the tiles are diagonal and return a solid tile.
            if ((quad[0] == 1 || quad[0] == 2) && (quad[1] == 1 || quad[1] == 2) && (quad[2] == 1 || quad[2] == 2) && (quad[3] == 1 || quad[3] == 2)) {
                for (k = 0; k < 4; k++) {
                    var d = quad[k] == 2 ? "d" : "";
                    quad[k] = "1." + (k + 1) + "00" + d;
                }
                return setQuad(x, y, quad);
            }

            for (k = 0; k < 4; k++) {
                //Select the subtile to analyze.
                var subTile = quad[k];
                //If the subtile is blank, try to close an angle & rotate clockwise 90 degrees.
                if (subTile == 0)
                    addAngle(!openAngle, 2);
                //If the subtile is solid, try to open an angle & rotate clockwise 90 degrees.
                else if (subTile == 1 || subTile == 2)
                    addAngle(openAngle, 2);
                //If the subtile is a clockwise triangle, try to close an angle, rotate clockwise 45 degrees, open an angle & rotate clockwise 45 degrees.
                else if (subTile == 3) {
                    addAngle(!openAngle, 1);
                    addAngle(openAngle, 1);
                }
                //If the subtile is a counter clockwise triangle, try to open an angle, rotate clockwise 45 degrees, close an angle & rotate clockwise 45 degrees.
                else if (subTile == 4) {
                    addAngle(openAngle, 1);
                    addAngle(!openAngle, 1);
                }
            }

            //If we started on an open angle, shift the array so the first number is where an angle opens.
            if (offset)
                angles.push(angles.shift());
            //If we missed the first angle because it was 0, add it.
            else if (openAngle)
                angles.push(0);

            //Iterate through each pair of angles and check which subtiles they span.
            for (k = 0; k < angles.length; k += 2) {
                for (l = 0; l < 4; l++) {
                    //Offset the angle so that 0 is the counter clockwise edge of the selected subtile.
                    var open = (angles[k] + 6 * l) % 8,
                        close = (angles[k + 1] + 6 * l) % 8;
                    //If the open or close angle falls within the subtile then set it to 1.[quadrant].[open angle].[close angle] & d if the corner is diagonal.
                    if (open < close && (open < 2 || close == 2 || close == 1) || open > close && (close > 0 || open < 2)) {
                        var diagonal = quad[l] == 2 ? "d" : "";
                        quad[l] = "1." + (l + 1) + angles[k] + angles[k + 1] + diagonal;
                    }
                }
            }

            setQuad(x, y, quad);

            function addAngle(open, increment) {
                //if the angle is already in the correct state (open or closed), only increment the angle position.
                if (!open) {
                    angles.push(angle);
                    openAngle = !openAngle;
                }
                angle += increment;
            }
        }
    }

