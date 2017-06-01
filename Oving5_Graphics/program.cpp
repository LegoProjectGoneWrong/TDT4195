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

//To get Pi
#define _USE_MATH_DEFINES
#include <math.h>
const float pi = float(M_PI);

const glm::vec3 x_axis(1,0,0);
const glm::vec3 y_axis(0,1,0);
const glm::vec3 z_axis(0,0,1);


glm::vec4 position(0,0,1,1); //startposition
glm::vec4 orientation(0,0,-1,0); //orientation down z-axis
glm::vec4 up_vector(0,1,0,0);

glm::mat4x4 MVP(1.0); //initiate MVP as identity matrix
glm::mat4x4 projectionMatrix;
glm::mat4x4 modelMatrix(1.0);
void updateMVP();


unsigned int setupVBO(float* vertices,int vertices_len,int* indices,int indices_len,float* colors,int colors_len){
    //Creates and binds VAO, referenced in array
    GLuint arrayID;
    glGenVertexArrays(1,&arrayID);
    glBindVertexArray(arrayID);

    //creates buffer and binds it
    GLuint vertexID;
    glGenBuffers(1,&vertexID);
    glBindBuffer(GL_ARRAY_BUFFER,vertexID);

    //Finds vertice lengthm and pushes the data to the buffer
    glBufferData(GL_ARRAY_BUFFER,vertices_len,vertices,GL_STATIC_DRAW); 

    //sets Vertext Attribute Pointer and enables the VBO
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,0);
    glEnableVertexAttribArray(0);
    
    //creates the Index Buffer
    GLuint indicesID;
    glGenBuffers(1,&indicesID);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,indicesID);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices_len,indices,GL_STATIC_DRAW);
    
    //create colors
    GLuint colorID;
    glGenBuffers(1,&colorID);
    glBindBuffer(GL_ARRAY_BUFFER,colorID);
    glBufferData(GL_ARRAY_BUFFER,colors_len,colors,GL_STATIC_DRAW);

    //sets pointer and enables
    glVertexAttribPointer(1,4,GL_FLOAT,GL_FALSE,0,0);
    glEnableVertexAttribArray(1);

    return arrayID;
}


void build_pyramid_other_coordinates(unsigned int& array,unsigned int& num_indices){
   float vertices[]={
      45.0f,90.0f,45.0f, //top
      10.0f,10.0f,10.0f, //south_west
      90.0f,10.0f,10.0f, //south_east
      10.0f,10.0f,90, //north_west
      90,10.0f,90 //north_east
    };


    int indices[] = {
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

    projectionMatrix = glm::ortho(0.0f,100.0f,0.0f,100.0f,0.0f,-100.0f);

  //overrides orthograpchig projection to  perspective
  //adds perspective, with nearplane to 0.2 as 1 was way to long to the back
	//projectionMatrix = glm::perspective(pi/2, 1.33f, 0.1f, 100.0f);

    
 
    array = setupVBO(vertices,sizeof(vertices),indices,sizeof(indices),colors,sizeof(colors));
    num_indices = sizeof(indices);
}

void build_pyramid(unsigned int& array,unsigned int& num_indices){
    float vertices[]={
      0,1,0, //top
      -1,-1,-1, //south_west
      1,-1,-1, //south_east
      -1,-1,1, //north_west
      1,-1,1 //north_east
    };

    int indices[] = {
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
    projectionMatrix = glm::perspective(pi/2, 1.33f, 0.1f, 100.0f);
    //adds perspective, with nearplane to 0.2 as 1 was way to long to the back
 
    array = setupVBO(vertices,sizeof(vertices),indices,sizeof(indices),colors,sizeof(colors));
    num_indices = sizeof(indices);
}
void build_triangles(unsigned int& array,unsigned int& num_indices){
	  projectionMatrix = glm::perspective(pi/2, 1.33f, 0.1f, 100.0f);

    float vertices[]={
      0,1,0,
      -0.5,0,0,
      0.5,0,0,

      -0.5,0,0,
     -1,-1,0,
      0,-1,0,

      0.5,0,0,
      0,-1,0,
      1,-1,0,

      -0.25,-0.15,0,
      -0.25,-0.30,0,
      0.375,-0.225,0,

      0.25,-0.15,0,
      0.25,-0.30,0,
      -0.375,-0.225,0
    };


    int indices[] = {
      0,1,2,
      3,4,5,
      6,7,8,
      9,10,11,
      12,14,13 //had to flip to make it show, hence 14 and 13 in that order
    };

    float colors[] = {
        0,0,0,1,
        1,1,0,1,
        0,0,1,1,

        1,0,0,1,
        0,1,0,1,
        0,1,1,1,

        1,0.3,1,
        1,0,1,1,
        1,1,1,1,
        
        0.7,  0.1,  0.9,  0,
        0.6,  0.6,  0.6,  0.6,
        0.6,  0.8,  0,    0.6,

        0.6,  0.1,  0.4,  0.6,
        0.3,  0.4,  0.8,  0.6,
        0.6,  0,    1,    0.6

    };
 
    array = setupVBO(vertices,sizeof(vertices),indices,sizeof(indices),colors,sizeof(colors));
    num_indices = sizeof(indices);
}

void runProgram(GLFWwindow* window){
    // Set GLFW callback mechanism(s)
    glfwSetKeyCallback(window, keyboardCallback);

    // Enable depth (Z) buffer (accept "closest" fragment)
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);

    // Configure miscellaneous OpenGL settings
    glEnable(GL_CULL_FACE);

    // Set default colour after clearing the colour buffer
    glClearColor(0.3f, 0.3f, 0.4f, 1.0f);

    // Set up your scene here (create Vertex Array Objects, etc.)
    // premaking these as I am returning 2 variables
    unsigned int array,num_indices;
    //build_triangles(array,num_indices);
    build_pyramid(array,num_indices);

    //builds the pyramids in 100,100,100 space, does not work with perspective
    //build_pyramid_other_coordinates(array,num_indices);
   
    //enable alpha
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_BLEND);

    //setup and activate shaders 
    Gloom::Shader shader;
    shader.makeBasicShader("../gloom/shaders/simple.vert","../gloom/shaders/simple.frag");  
    shader.activate();
    if(!shader.isValid()){
      printf("Shader not Valid");
    }
    updateMVP();
    

    // Rendering Loop
    int i = 0;
    while (!glfwWindowShouldClose(window))
    {
        // Clear colour and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Draw your scene here

        //forwards the transformation for task 2b
        glUniform1f(2,(float)sin(i/500.0));
        i++;

        //sends in the MVP transformation
        glUniformMatrix4fv(3,1,false,glm::value_ptr(MVP));

        glBindVertexArray(array);
        glDrawElements(GL_TRIANGLES,num_indices,GL_UNSIGNED_INT,0); 
        // Handle other events
        glfwPollEvents();

        // Flip buffer
        glfwSwapBuffers(window);
    }
}
void updateMVP() {
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
  


  //MVP = viewMatrix;
  MVP = projectionMatrix * viewMatrix * modelMatrix;
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
    updateMVP();
}

