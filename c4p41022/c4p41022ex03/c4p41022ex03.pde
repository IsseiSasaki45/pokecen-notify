PImage mapImage; 
Table dataTable;
int rowCount;
float dataMax=MIN_FLOAT;
float dataMin=MAX_FLOAT;
boolean modeFlag=true;

void mousePressed(){
  if(modeFlag){
    modeFlag=false;
  }
  else{
    modeFlag=true;
  }
}

void setup(){
  size(700,530);
  mapImage=loadImage("japan.png");
  dataTable=loadTable("location.tsv");
  rowCount=dataTable.getRowCount();
  PFont font=createFont("MS Mincho",24);
  textFont(font);
  
  
  for(int row=0;row<rowCount;row++){
    float value=dataTable.getFloat(row,3);
    if(value>dataMax){
      dataMax=value;
    }
    if(value<dataMin){
      dataMin=value;
    }
  }
}

void draw(){
  image(mapImage,0,0);
  for(int row=0;row<rowCount;row++){
    float people=dataTable.getFloat(row,3);
    float percent=norm(people,dataMin,dataMax);
    fill(255,0,0,255*percent);
    ellipse(dataTable.getInt(row,1),dataTable.getInt(row,2),10,10);
  }
  
  fill(0,0,0);
  if(modeFlag==true){
    text("都道府県表示モード",0,40);
  }
  else{
    text("人数表示モード",0,40);
  }
  
  for(int row=0;row<rowCount;row++){
    int x=dataTable.getInt(row,1);
    int y=dataTable.getInt(row,2);
    float distance=dist(x,y,mouseX,mouseY);
    
    if(distance<=5){
      fill(0,0,0);
      if(modeFlag==true){
        text(dataTable.getString(row,0),x,y);
      }
      else{
        text(dataTable.getString(row,3)+"人",x,y);
      }
    }
  }
}
