dir1 = "C:/Users/obiswas/OneDrive - IDEXX/OneDrive/3cc_local/images"
dir2 = "C:/Users/obiswas/OneDrive - IDEXX/OneDrive/3cc_local/macro_output"
run("Plots...", "width=1000 height=340 font=14 draw_ticks list minimum=0 maximum=0 interpolate");

function action(input, output, filename) {
        open(input + filename);
        makeLine(154,198,1696,192,1700,404,122,410,134,614,1700,588,1698,796,134,808,130,1016,1700,988);
        run("Plot Profile");
        selectWindow("Plot Values");
		saveAs("Results", "path/to/desired/output" + filename + ".csv" );
}


list = getFileList(input);
for (i = 0; i < list.length; i++){
        action(input, output, list[i]);
}

run("Quit")