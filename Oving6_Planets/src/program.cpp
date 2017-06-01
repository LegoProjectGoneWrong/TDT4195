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

#define SLICES 80
#define NUM_INDICES SLICES*SLICES*2*3

const glm::vec3 x_axis(1,0,0);
const glm::vec3 y_axis(0,1,0);
const glm::vec3 z_axis(0,0,1);



glm::vec4 position(0,0,7,1); //startposition
glm::vec4 orientation(0,0,-1,0); //orientation down z-axis
glm::vec4 up_vector(0,1,0,0);

glm::vec3 null_vector(0,0,0);
glm::mat4x4 identity(1.0);

glm::mat4x4 VP(1.0); //initiate VP as identity matrix
glm::mat4x4 projectionMatrix = glm::perspective(pi/2,1.33f,0.1f,100.0f);
glm::mat4x4 modelMatrix(1.0);

void updateVP();
void setWindowSettings(GLFWwindow* window);
unsigned int setupVAO(float* vertices,unsigned int* indices, float* colors,int triangleCount);
unsigned int  build_pyramid(unsigned int& array,unsigned int& num_indices);

SceneNode* createPlanet(float X, float Y, float Z,float R,float G,float B,float scale, float rotSpeed, glm::vec3 rotAxis,float selfRotSpeed,glm::vec3 selfRotAxis,SceneNode* parent){
  SceneNode* planet = createSceneNode();
  addChild(parent,planet);
  planet-> vertexArrayObjectID = createCircleVAO(SLICES,SLICES,R,G,B);
  planet->x=-X;
  planet->y=Y;
  planet->z=Z;
  planet->scaleFactor = 0.5*scale;
  planet->rotationSpeedRadians = 0.5*rotSpeed;
  planet->rotationDirection=rotAxis;
  planet->selfRotationSpeedRadians = 0.3*selfRotSpeed;
  planet->selfRotationDirection=selfRotAxis;
  return planet;
}

SceneNode* createSystem(){
  SceneNode* sun = createSceneNode();
  sun-> vertexArrayObjectID = createCircleVAO(SLICES,SLICES,4,2,1); //double colors due to the sun not being shaded, hence 0.5 scaled
  sun->main_planet = true;
  sun->scaleFactor = 2;
  sun->selfRotationSpeedRadians = 0.02;
  //earth scale = 1, earth rotation speed = 1, earth self roation = 1
  //planet                              x,y,z, R   G   B   S   rs  ra    ss    sa  parent
  SceneNode* earth       = createPlanet(8,0,0,0.5,0.5,1.0,1.0,1.0,y_axis,1.0,y_axis,sun);
  SceneNode* moon        = createPlanet(1,0,0,0.4,0.2,0.2,0.2,2.0,y_axis,0.0,y_axis,earth);

  SceneNode* venus       = createPlanet(0,0,-3,0.6,0.6,0.6,0.5,3.0,y_axis,2.0,y_axis,sun);
  SceneNode* mercury     = createPlanet(5,0,0,0.9,0.6,0.0,0.8,2.0,y_axis,2.0,x_axis,sun);

  SceneNode* jupiter     = createPlanet(0,0,-10,0.5,0.6,0.6,2,0.7,y_axis,0.7,y_axis,sun);
  SceneNode* jup_moon1   = createPlanet(2,0,0,0.4,0.2,0.2,0.2,2.0,y_axis,0.3,y_axis,jupiter);
  SceneNode* jup_moon2   = createPlanet(0,0,3,0.4,0.2,0.2,0.6,3.0,y_axis,0.9,y_axis,jupiter);
  SceneNode* jup_moon3   = createPlanet(0,2,0,0.4,0.2,0.2,0.2,2.0,x_axis,2.0,x_axis,jupiter);

  glm::vec3 p_axis(1,1,0);
  SceneNode* pluto       = createPlanet(7,7,0,0.8,0.0,0.9,1.0,1.0,p_axis,2.0,x_axis,sun);
  
  glm::vec3 t_axis(5,-5,0);
  SceneNode* twin_p       = createPlanet(5,-5,0,0.8,0.0,0.9,0.0,1.0,t_axis,2.0,x_axis,sun);
  SceneNode* twin1       = createPlanet(0.5,0,0,0.8,0.0,0.5,0.4,6.0,y_axis,2.0,x_axis,twin_p);
  SceneNode* twin2       = createPlanet(-0.5,0,0,0.8,0.0,0.5,0.4,3.0,y_axis,2.0,x_axis,twin_p);
  return sun;
}
void updatePlanetPosition(SceneNode* planet,float time_elapsed,glm::mat4 parent_pos){
  glm::vec4 pos = {planet->x,planet->y,planet->z,1};
  pos = pos*glm::rotate(time_elapsed*planet->rotationSpeedRadians,-planet->rotationDirection);
  planet->x=pos.x;
  planet->y=pos.y;
  planet->z=pos.z;
  planet->currentRotation=planet->currentRotation + time_elapsed*3.0f;
  glm::mat4 planet_pos = glm::translate(glm::vec3(-pos))*parent_pos;
  glm::mat4 selfRotation = glm::rotate(planet->currentRotation*planet->selfRotationSpeedRadians,planet->selfRotationDirection); 
  planet->currentTransformationMatrix = planet_pos*selfRotation;
  for(int i = 0; i<planet->children.size();i++){
    updatePlanetPosition(planet->children[i],time_elapsed,planet_pos);
  }
}
void renderPlanet(SceneNode* planet){
  glm::mat4 model = planet->currentTransformationMatrix * glm::scale(glm::vec3(planet->scaleFactor));
  glBindVertexArray(planet->vertexArrayObjectID);
  glm::mat4 MVP = VP*model;
  glUniformMatrix4fv(3,1,false,glm::value_ptr(MVP));

  if(planet->main_planet){ //if sun no shade shall be added

    glUniformMatrix4fv(4,1,false,glm::value_ptr(identity)); //model
    glUniformMatrix4fv(2,1,false,glm::value_ptr(null_vector)); //position
  }
  else{
    glUniformMatrix4fv(4,1,false,glm::value_ptr(model));
  }
  glDrawElements(GL_TRIANGLES,NUM_INDICES,GL_UNSIGNED_INT,0); 
  for(int i = 0; i<planet->children.size();i++){
    renderPlanet(planet->children[i]);
  }
}

void runProgram(GLFWwindow* window){
    setWindowSettings(window);
    SceneNode* main_planet;
    main_planet = createSystem();
    unsigned int array = createCircleVAO(SLICES,SLICES,0,1,0);

    updateVP();
    while (!glfwWindowShouldClose(window))
    {
        // Clear colour and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Draw your scene here
        updatePlanetPosition(main_planet,getTimeDeltaSeconds(),glm::mat4x4(1.0)); 
        renderPlanet(main_planet);
        

        //sends in the VP transformation
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
	glm::mat4x4 rotation_x = glm::rotate(atan2(-direction.x, direction.z), y_axis);
	direction = rotation_x * direction;

  //rotates camera to y=0 by revoling around x-axis with formula found on internet
	glm::mat4x4 rotation_y = glm::rotate(atan(direction.y/ direction.z), x_axis);
	direction = rotation_y *direction;
  
  //rotate camera to z=-1 by revolving around y-axis if its set to z=1
	glm::mat4x4 rotation_z = glm::mat4(1.0);
	if (direction.z > 0)
		rotation_z = glm::rotate(pi, y_axis);
	direction = rotation_z * direction;

  //compute full rotation transformation
	glm::mat4x4 rotation_transformation = rotation_z * rotation_y * rotation_x;

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
unsigned int  build_pyramid(unsigned int& array,unsigned int& num_indices){
    float vertices[]={
      0,1,0, //top
      -1,-1,-1, //south_west
      1,-1,-1, //south_east
      -1,-1,1, //north_west
      1,-1,1 //north_east
    };

    unsigned int indices[] = {
      3,1,2, //bottom square
      3,2,4,
      2,1,0, //walls of pyramid
      1,3,0,
      3,4,0,
      4,2,0
    };

    float colors[] = {
        1.000f, 1.000f, 1.000f,0.8,
        0.000f, 1.000f, 0.000f,0.8,
        0.000f, 0.000f, 1.000f,0.8,
        1.000f, 0.000f, 0.000f,0.8,
        1.000f, 1.0f,0.0f,0.8
    };
    
    //projectionMatrix = glm::ortho(-1,1,-1,1,-1,1);
    //projectionMatrix = glm::perspective(pi/2, 1.33f, 0.1f, 100.0f);
    //adds perspective, with nearplane to 0.2 as 1 was way to long to the back
 
    //array = setupVAO(vertices,indices,colors,6);
    num_indices = sizeof(indices);
    return array;
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
    else if (key == GLFW_KEY_UP){ //moves up
      position = glm::translate(0.1f*y_axis)*position;
    }
    else if (key == GLFW_KEY_DOWN){ //moves down
      position = glm::translate(-0.1f*y_axis)*position;
    }
    else if (key == GLFW_KEY_LEFT){ //moves to the left, along right_vector
      position = glm::translate(-0.1f*right_vector)*position;
    }
    else if (key == GLFW_KEY_RIGHT){ //moves to the right, along right_vector
      position = glm::translate(0.1f*right_vector)*position;
    }
    else if (key == GLFW_KEY_ENTER){ //moves forward, along current orientation
      position = position+0.1f*orientation;
    }
    else if (key == GLFW_KEY_BACKSPACE){ //moves backwards, along current orientation
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
    //updates the view matrix after a keyboard interrupt
    printf("Moving \n");
    updateVP();
}

