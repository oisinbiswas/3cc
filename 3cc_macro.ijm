input = "C:/Users/obiswas/OneDrive - IDEXX/OneDrive/3qc/transition_testing/";
output = "C:/Users/obiswas/OneDrive - IDEXX/OneDrive/3qc/transition_output/";
run("Plots...", "width=1000 height=340 font=14 draw_ticks list minimum=0 maximum=0 interpolate");

function action(input, output, filename) {
        open(input + filename);
        makeLine(234,396,1612,416,1610,540,244,510,238,640,1606,636,1590,754,238,740,240,874,1586,868);
        run("Plot Profile");
        selectWindow("Plot Values");
		saveAs("Results", "C:/Users/obiswas/OneDrive - IDEXX/OneDrive/3qc/transition_output/" + filename + ".csv" );
}


list = getFileList(input);
for (i = 0; i < list.length; i++){
        action(input, output, list[i]);
}

