// Local headers
#include "program.hpp"
#include "gloom/gloom.hpp"
#include "gloom/shader.hpp"
#include "glm/glm.hpp"
#include "glm/gtc/type_ptr.hpp"
#include <glm/mat4x4.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtx/transform.hpp>
#include <glm/vec3.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <algorithm> //min function
#include <windows.h>
#define 	GLFW_KEY_RIGHT   262
#define 	GLFW_KEY_LEFT   263
#define 	GLFW_KEY_DOWN   264
#define 	GLFW_KEY_UP   265
#define 	GLFW_KEY_ENTER   257
#define 	GLFW_KEY_BACKSPACE   259
#define 	GLFW_KEY_A   65
#define 	GLFW_KEY_D   68
#define 	GLFW_KEY_S   83
#define 	GLFW_KEY_W   87
#define   GLFW_KEY_SPACE 32
#define   GLFW_KEY_M 77
#define   GLFW_KEY_N 78


#define SLICES 80
#define NUM_INDICES SLICES*SLICES*2*3
#define BOARD_DEPTH 8
#define BOARD_WIDTH 8

const glm::vec3 x_axis(1,0,0);
const glm::vec3 y_axis(0,1,0);
const glm::vec3 z_axis(0,0,1);

glm::vec4 position(0,0.5,2,1); //startposition
glm::vec4 orientation(0,0,-1,0); //orientation down z-axis
glm::vec4 up_vector(0,1,0,0);

glm::vec3 null_vector(0,0,0);
glm::mat4x4 identity(1.0);

glm::mat4x4 VP(1.0); //initiate VP as identity matrix
glm::mat4x4 projectionMatrix = glm::perspective(pi/2,1.33f,0.1f,100.0f);
glm::mat4x4 modelMatrix(1.0);

bool moving = false;
bool waiting_for_press = true;
int hl_figure = 0;
int hl_tile = 0;
int num_figures = 0;
int num_tiles = BOARD_DEPTH*BOARD_WIDTH;

glm::vec4 bright_overlay(1.0,1.0,1.0,0.0);
glm::vec4 no_overlay(0.0f,0.0f,0.0f,0.0f);

bool* figure_tiles = new bool[num_tiles];
float move_x,move_z,curr_x,curr_z,speed_x,speed_z;
int moving_incremental;
SceneNode* reference_node;

void updateVP();
void setWindowSettings(GLFWwindow* window);
unsigned int setupVAO(float* vertices,unsigned int* indices, float* colors,int triangleCount);
unsigned int  build_pyramid(unsigned int& array,unsigned int& num_indices);

void createStar(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createStarVAO(R,G,B); 
  star->scaleFactor=0.3;
  star->triangleCount = 8*2;
}
void createBox(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createBoxVAO(R,G,B); 
  star->scaleFactor=0.2;
  star->triangleCount = 8*2;
}
void createHexagon(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createHexagonVAO(R,G,B); 
  star->scaleFactor=0.3;
  star->triangleCount = 8*6;
}
void createWeirdTriangle(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createWeirdTriangleVAO(R,G,B);
  star->scaleFactor=0.3;
  star->triangleCount = 8*4;
}
void createPacman(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createPacmanVAO(R,G,B);
  star->scaleFactor=0.3;
  star->triangleCount = 8*9;
}
void createStandardTriangle(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createStandardTriangleVAO(R,G,B);
  star->scaleFactor=0.3;
  star->triangleCount = 8*9;
}
void createParallelogram(SceneNode* star, float R, float G, float B){
  star->vertexArrayObjectID = createParallelogramVAO(R,G,B);
  star->scaleFactor=0.3;
  star->triangleCount = 8*2;
}
void createFigure(int type, SceneNode* reference_node,int x, int z ,float R, float G, float B){
  int position = BOARD_DEPTH*x+z;
  if(reference_node->children[position]->is_vacant){
    num_figures++;
    reference_node->children[position]->is_vacant=false;
    SceneNode* figure = createSceneNode();
    figure->belongs_to_tile = position;
    addChild(reference_node,figure);
    figure->y=-0.01;
    figure->scaleFactor=0.3;
    figure->x = -0.5-x;
    figure->z= 0.5+z;
    figure->selfRotationSpeedRadians = 0.1;
    figure->currentRotation = random();
    if(type==1){
      createStar(figure,R,G,B);
    }
    else if(type==2){
      createBox(figure,R,G,B);
    }
    else if(type==3){
      createHexagon(figure,R,G,B);
    }
    else if(type==4){
      createWeirdTriangle(figure,R,G,B);
    }
    else if(type==5){
      createPacman(figure,R,G,B);
    }
    else if(type==6){
      createStandardTriangle(figure,R,G,B);
    }
    else if(type==7){
      createParallelogram(figure,R,G,B);
    }

  }
  else{
    printf("Not a vacant tile");
  }
}

void addFigures(SceneNode* reference_node){
  createFigure(1,reference_node,0,0,1,0,1);
  createFigure(1,reference_node,1,1,1,0,0.0);
  createFigure(2,reference_node,7,2,0,0,1);
  createFigure(3,reference_node,0,1,1,1,0);
  createFigure(4,reference_node,0,6,1,1,0);
  createFigure(5,reference_node,1,3,1,1,0);
  createFigure(6,reference_node,2,2,0,1,0);
  createFigure(7,reference_node,2,1,0,1,0);
}

SceneNode* buildBoard(){
  reference_node = createSceneNode();
  reference_node->x=-(BOARD_DEPTH/2.0);
  reference_node->z=0;
  reference_node->y=-3;
  int x,z;
  for(x=0;x<BOARD_WIDTH;x+=1){
    for(z=0;z<BOARD_DEPTH;z+=1){
    SceneNode* square = createSceneNode();
    if((x+z)%2==0){
      square->vertexArrayObjectID = createSquareVAO(1,1,2,0,0);
    }
    else{
      square->vertexArrayObjectID = createSquareVAO(1,1,0.0,0.0,2);
    }
    addChild(reference_node,square);
    square->x=-x;
    square->z=z;
    square->triangleCount=2;
    }
  }
  printf("%d",num_tiles);
  return reference_node;
}

void updateMovingFigurePosition(SceneNode* current_figure,glm::vec3 ref_pos, float time_elapsed){
  if(moving_incremental<300){
    current_figure->y = current_figure->y -0.005f;
  }
  else if (moving_incremental<600){
    float curr_x = current_figure->x;
    float curr_z = current_figure->z;
    current_figure->x = curr_x + (move_x-curr_x)/50;
    current_figure->z = curr_z + (move_z-curr_z)/50;
  }
  else if(moving_incremental<900){
    current_figure->x=move_x;
    current_figure->z=move_z;
    current_figure->y = current_figure->y +0.005f;
  }
  else{
    current_figure->y=0.01;
    moving=false;
  }
  moving_incremental++;
}

void renderBoard(SceneNode* reference_node,float time_elapsed){
  glm::vec3 ref_pos = {reference_node->x,reference_node->y,reference_node->z};
  SceneNode* current_tile;
  for(int i = 0; i<num_tiles;i++){
    current_tile = reference_node->children[i];
    glm::vec4 pos = {current_tile->x,current_tile->y,current_tile->z,1};
    glm::mat4 model = glm::translate(glm::vec3(-pos))*glm::translate(ref_pos);
    glUniformMatrix4fv(4,1,false,glm::value_ptr(model));
    glm::mat4 MVP = VP*model;
    glUniformMatrix4fv(3,1,false,glm::value_ptr(MVP)); //model

    if(i==hl_tile){
      glUniform4fv(5,1,glm::value_ptr(bright_overlay));
    }
    else{
      glUniform4fv(5,1,glm::value_ptr(no_overlay));
    }
    glBindVertexArray(current_tile->vertexArrayObjectID);
    glDrawElements(GL_TRIANGLES,current_tile->triangleCount*3,GL_UNSIGNED_INT,0); 
  }
}

void renderFigures(SceneNode* reference_node,float time_elapsed){
  glm::vec3 ref_pos = {reference_node->x,reference_node->y,reference_node->z};
  SceneNode* current_figure;
  for(int i = num_tiles; i<reference_node->children.size();i++){
    current_figure = reference_node->children[i];
    if(i-num_tiles==hl_figure){
      current_figure->currentRotation=current_figure->currentRotation + time_elapsed*15.0f;
      glUniform4fv(5,1,glm::value_ptr(bright_overlay));
      if(moving){
        updateMovingFigurePosition(current_figure,ref_pos,time_elapsed);
      }
    }
    else{
      current_figure->currentRotation=current_figure->currentRotation + time_elapsed*3.0f;
      glUniform4fv(5,1,glm::value_ptr(no_overlay));
    }
    glm::vec4 pos = {current_figure->x,current_figure->y,current_figure->z,1};
    glm::mat4 model = glm::translate(glm::vec3(-pos))*glm::translate(ref_pos)*glm::scale(glm::vec3(current_figure->scaleFactor));
    model = model*glm::rotate(current_figure->currentRotation*current_figure->selfRotationSpeedRadians,y_axis);

    glUniformMatrix4fv(4,1,false,glm::value_ptr(model));
    glm::mat4 MVP = VP*model;
    glUniformMatrix4fv(3,1,false,glm::value_ptr(MVP)); //model
    glBindVertexArray(current_figure->vertexArrayObjectID);
    glDrawElements(GL_TRIANGLES,current_figure->triangleCount*3,GL_UNSIGNED_INT,0); 
  }
}


void runProgram(GLFWwindow* window){
    setWindowSettings(window);
    SceneNode* main_planet;
    unsigned int square = createSquareVAO(1,1,0.8,0.5,1);
    unsigned int array = createCircleVAO(SLICES,SLICES,0,1,0);
    unsigned int star = createStarVAO(1,1,0);
    SceneNode* reference_node = buildBoard();
    addFigures(reference_node);

    updateVP();
    float time_elapsed;
    int i = 0;
    while (!glfwWindowShouldClose(window))
    {
        // Clear colour and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        time_elapsed=getTimeDeltaSeconds();
        i++;
        float k = abs(sin(0.02*i/pi))*0.4f;
        bright_overlay = {k,k,k,1};

        glUniform4fv(5,1,glm::value_ptr(no_overlay));
        renderBoard(reference_node,time_elapsed);
        renderFigures(reference_node,time_elapsed);       

        // Handle other events
        glfwPollEvents();

        // Flip buffer
        glfwSwapBuffers(window);
    }
}
unsigned int setupVAO(float* vertices,unsigned int* indices, float* colors,float* normals,int triangleCount){
    //Creates and binds VAO, referenced in array
    GLuint arrayID;
    glGenVertexArrays(1,&arrayID);
    glBindVertexArray(arrayID);

    //creates buffer and binds it
    GLuint vertexID;
    glGenBuffers(1,&vertexID);
    glBindBuffer(GL_ARRAY_BUFFER,vertexID);
    glBufferData(GL_ARRAY_BUFFER,sizeof(float)*triangleCount*3*3,vertices,GL_STATIC_DRAW); 

    //sets Vertext Attribute Pointer and enables the VBO
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,0);
    glEnableVertexAttribArray(0);
    
    //creates the Index Buffer
    GLuint indicesID;
    glGenBuffers(1,&indicesID);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,indicesID);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(unsigned int)*triangleCount*3,indices,GL_STATIC_DRAW);
    
    //create colors
    GLuint colorID;
    glGenBuffers(1,&colorID);
    glBindBuffer(GL_ARRAY_BUFFER,colorID);
    glBufferData(GL_ARRAY_BUFFER,sizeof(float)*triangleCount*12,colors,GL_STATIC_DRAW);
    //sets pointer and enables
    glVertexAttribPointer(1,4,GL_FLOAT,GL_FALSE,0,0);
    glEnableVertexAttribArray(1);

    //create normals
    GLuint normalID;
    glGenBuffers(1,&normalID);
    glBindBuffer(GL_ARRAY_BUFFER,normalID);
    glBufferData(GL_ARRAY_BUFFER,sizeof(float)*triangleCount*9,colors,GL_STATIC_DRAW);
    glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,0,0);
    glEnableVertexAttribArray(2);

    return arrayID;
}
void updateVP() {
  //direction of current view
	glm::vec4 direction(orientation);

  //rotates camera to x=0 by revolving around y-axis, formula found on internet
	glm::mat4x4 rotatioBOARD_DEPTH = glm::rotate(atan2(-direction.x, direction.z), y_axis);
	direction = rotatioBOARD_DEPTH * direction;

  //rotates camera to y=0 by revoling around x-axis with formula found on internet
	glm::mat4x4 rotation_y = glm::rotate(atan(direction.y/ direction.z), x_axis);
	direction = rotation_y *direction;
  
  //rotate camera to z=-1 by revolving around y-axis if its set to z=1
	glm::mat4x4 rotatioBOARD_WIDTH = glm::mat4(1.0);
	if (direction.z > 0)
		rotatioBOARD_WIDTH = glm::rotate(pi, y_axis);
	direction = rotatioBOARD_WIDTH * direction;

  //compute full rotation transformation
	glm::mat4x4 rotation_transformation = rotatioBOARD_WIDTH * rotation_y * rotatioBOARD_DEPTH;

  //finds current up_vector of this transformation
	glm::vec4 up = rotation_transformation * up_vector;

  //finds transformation that rotates to "up"
	glm::mat4x4 rotate_Up = glm::rotate(atan2(up.x, up.y), z_axis);
  //rotates to up 
	rotation_transformation = rotate_Up * rotation_transformation;

	// Tranformation for moving to eye view
  glm::vec3 eye_view = -glm::vec3(position);
  //computes full transformation from rotation and eye-view transformations
  glm::mat4x4 viewMatrix = rotation_transformation * glm::translate(eye_view);
  
  //VP = viewMatrix;
  VP = projectionMatrix * viewMatrix * modelMatrix;
}
void initMovingFigure(){
  SceneNode* current_node = reference_node->children[hl_figure+num_tiles]; 
  SceneNode* current_tile = reference_node->children[hl_tile]; 
  current_tile->is_vacant=false;
  curr_x = current_node->x;
  curr_z = current_node->z; 
  int curr_tile = int(abs(curr_x))*BOARD_DEPTH+int(curr_z);
  reference_node->children[curr_tile]->is_vacant=true;
  move_x = current_tile->x-0.5;
  move_z = current_tile->z+0.5;
  speed_x=(move_x-curr_x)/200;
  speed_z=(move_z-curr_z)/200;
  moving_incremental=0;
  moving=true; 
}
void setWindowSettings(GLFWwindow* window){
    // Set GLFW callback mechanism(s)
    glfwSetKeyCallback(window, keyboardCallback);
    // Enable depth (Z) buffer (accept "closest" fragment)
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    // Configure miscellaneous OpenGL settings
    glEnable(GL_CULL_FACE);
    // Set default colour after clearing the colour buffer
    glClearColor(0.1f, 0.1f, 0.2f, 1.0f);
    //enable alpha
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_BLEND);

    Gloom::Shader shader;
    shader.makeBasicShader("../gloom/shaders/simple.vert","../gloom/shaders/simple.frag");  
    shader.activate();
    //setup and activate shaders 
    if(!shader.isValid()){
      printf("Shader not Valid");
    }
}
void keyboardCallback(GLFWwindow* window, int key, int scancode,int action, int mods){
    //rigt vector for current state, perpendicular to orinetation and up-vector
    glm::vec3 right_vector = glm::cross(glm::vec3(orientation),glm::vec3(up_vector));

    // Use escape key for terminating the GLFW window
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS){
        glfwSetWindowShouldClose(window, GL_TRUE);
    }
    //camera position movements
    else if (key == GLFW_KEY_ENTER){ //moves up
      position = glm::translate(0.1f*y_axis)*position;
    }
    else if (key == GLFW_KEY_BACKSPACE){ //moves down
      position = glm::translate(-0.1f*y_axis)*position;
    }
    else if (key == GLFW_KEY_LEFT){ //moves to the left, along right_vector
      position = glm::translate(-0.1f*right_vector)*position;
    }
    else if (key == GLFW_KEY_RIGHT){ //moves to the right, along right_vector
      position = glm::translate(0.1f*right_vector)*position;
    }
    else if (key == GLFW_KEY_UP){ //moves forward, along current orientation
      position = position+0.1f*orientation;
    }
    else if (key == GLFW_KEY_DOWN){ //moves backwards, along current orientation
      position = position-0.1f*orientation;
    }
   //rotational movements 
   //rotates either around right-vector or around y-axis
    else if (key == GLFW_KEY_W){ //looks up
      glm::mat4x4 rotation = glm::rotate(0.1f,right_vector);
      orientation = rotation*orientation;
      up_vector = rotation*up_vector; //updates up vector
    }
    else if (key == GLFW_KEY_S){ //looks down
      glm::mat4x4 rotation = glm::rotate(-0.1f,right_vector); 
      orientation = rotation*orientation;
      up_vector = rotation*up_vector;
    }
    else if (key == GLFW_KEY_A){ //looks left
      glm::mat4x4 rotation = glm::rotate(0.1f,y_axis);
      orientation = rotation*orientation;
      up_vector = rotation*up_vector; 
    }
    else if (key == GLFW_KEY_D){ //looks right
      glm::mat4x4 rotation = glm::rotate(-0.1f,y_axis);
      orientation = rotation*orientation;
      up_vector = rotation*up_vector;
    }
    //Commands for moving object¨
    else if(!moving && waiting_for_press){
      waiting_for_press=false;
      if (key == GLFW_KEY_SPACE){ //moves up
        if(reference_node->children[hl_tile]->is_vacant){
          initMovingFigure();
        }
        else{
          printf("Not vacant or moving");
        }
      }
      else if (key == GLFW_KEY_N){ //moves up
        hl_figure=(hl_figure+1)%num_figures;
        printf("Current figure%d",hl_figure);
      }
      else if (key == GLFW_KEY_M){ //moves up
        hl_tile=(hl_tile+1)%(num_tiles);
        printf("Current tile: %d",hl_tile);
      }
      else{
        waiting_for_press=true;
      }
    }
    else{
      waiting_for_press=true;
    }
    //updates the view matrix after a keyboard interrupt
    printf("Moving \n");
    updateVP();
}


