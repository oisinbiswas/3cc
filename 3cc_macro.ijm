input = "path/to/images";
output = "path/to/desired/output";
run("Plots...", "width=1000 height=340 font=14 draw_ticks list minimum=0 maximum=0 interpolate");

function action(input, output, filename) {
        open(input + filename);
        makeLine(234,396,1612,416,1610,540,244,510,238,640,1606,636,1590,754,238,740,240,874,1586,868);
        run("Plot Profile");
        selectWindow("Plot Values");
		saveAs("Results", "path/to/desired/output" + filename + ".csv" );
}


list = getFileList(input);
for (i = 0; i < list.length; i++){
        action(input, output, list[i]);
}

run("Quit")