PImage mapImage; 
Table dataTable;
int rowCount;
float dataMax=MIN_FLOAT;
float dataMin=MAX_FLOAT;
boolean modeFlag=true;
boolean changeFlag=false;

void mousePressed(){
  if(changeFlag){
    if(modeFlag){
      modeFlag=false;
    }
    else{
      modeFlag=true;
    }
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

void draw_ellipse(int x,int y,float percent){
  fill(255,0,0,255*percent);
  ellipse(x,y,10,10);
}

void draw_Text(int x,int y,String text){
  fill(0,0,0);
  text(text,x,y);
}

void draw(){
  changeFlag=false;
  
  image(mapImage,0,0);
  for(int row=0;row<rowCount;row++){
    int x=dataTable.getInt(row,1);
    int y=dataTable.getInt(row,2);
    float people=dataTable.getFloat(row,3);
    float percent=norm(people,dataMin,dataMax);
    float distance=dist(x,y,mouseX,mouseY);
    
    if(distance<=5){
      
      changeFlag=true;
      
      fill(0,0,255);
      ellipse(x,y,10,10);
      
      if(modeFlag){
        draw_Text(x,y,dataTable.getString(row,0));
      }
      else{
        text(dataTable.getString(row,3)+"人",x,y);
      }
    }
    else{
      draw_ellipse(x,y,percent);
    }
  }
  
  fill(0,0,0);
  if(modeFlag==true){
    draw_Text(0,40,"都道府県表示モード");
  }
  else{
    draw_Text(0,40,"人数表示モード");
  }
}
