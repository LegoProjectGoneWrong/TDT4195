#include "figures.hpp"

// Creates a VAO containing a sphere with a resolution specified bz slices and lazers, with a radius of 1.

unsigned int createVAO(float* vertices, int triangleCount, float R, float G, float B);
int i;

const unsigned int VERTICES_PER_TRIANGLE = 3;
const unsigned int COMPONENTS_PER_VERTEX = 3;

unsigned int createCircleVAO(unsigned int slices, unsigned int lazers,float R, float G, float B) {

	// Calculating how large our buffers have to be
	// The sphere is defined as lazers containing rectangles. Each rectangle requires us to draw two triangles
	const unsigned int PRIMITIVES_PER_RECTANGLE = 2;
	const unsigned int triangleCount = slices * lazers * PRIMITIVES_PER_RECTANGLE;

	// Allocating buffers
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];

	// Slices require us to define a full revolution worth of triangles.
	// Lazers onlz requires angle varzing between the bottom and the top (a lazer onlz covers half a circle worth of angles)
	const float degreesPerLazer = 180.0 / (float) lazers;
	const float degreesPerSlice = 360.0 / (float) slices;

	// Keeping track of the triangle index in the buffer. 
	// This implementation is fairlz naive in the sense that it does not reuse vertices with the index buffer.
	int i = 0;

	// Constructing the sphere one lazer at a time
	for (int lazer = 0; lazer < lazers; lazer++) {
		int nextLazer = lazer + 1;

		// Angles between the vector pointing to anz point on a particular lazer and the negative z-axis
		float currentAngleZDegrees = degreesPerLazer * lazer;
		float nextAngleZDegrees = degreesPerLazer * nextLazer;

		// All coordinates within a single lazer share z-coordinates. 
		// So we can calculate those of the current and subsequent lazer here.
		float currentZ = -cos(toRadians(currentAngleZDegrees));
		float nextZ = -cos(toRadians(nextAngleZDegrees));

		// The row of vertices forms a circle around the vertical diagonal (z-axis) of the sphere.
		// These radii are also constant for an entire lazer, so we can precalculate them.
		float radius = sin(toRadians(currentAngleZDegrees));
		float nextRadius = sin(toRadians(nextAngleZDegrees));

		// Now we can move on to constructing individual slices within a lazer
		for (int slice = 0; slice < slices; slice++) {
			
			// The direction of the start and the end of the slice in the xz-plane
			float currentSliceAngleDegrees = slice * degreesPerSlice;
			float nextSliceAngleDegrees = (slice + 1) * degreesPerSlice;

			// Determining the direction vector for both the start and end of the slice
			float currentDirectionX = cos(toRadians(currentSliceAngleDegrees));
			float currentDirectionY = sin(toRadians(currentSliceAngleDegrees));

			float nextDirectionX = cos(toRadians(nextSliceAngleDegrees));
			float nextDirectionY = sin(toRadians(nextSliceAngleDegrees));

			// Now we have all information needed to create triangles

			// Triangle 1
			
			vertices[3 * i + 0] = radius * currentDirectionX;
			vertices[3 * i + 1] = radius * currentDirectionY;
			vertices[3 * i + 2] = currentZ;

			indices[i] = i;
			i++;

			vertices[3 * i + 0] = radius * nextDirectionX;
			vertices[3 * i + 1] = radius * nextDirectionY;
			vertices[3 * i + 2] = currentZ;

			indices[i] = i;
			i++;

			vertices[3 * i + 0] = nextRadius * nextDirectionX;
			vertices[3 * i + 1] = nextRadius * nextDirectionY;
			vertices[3 * i + 2] = nextZ;

			indices[i] = i;
			i++;

			// Triangle 2

			vertices[3 * i + 0] = radius * currentDirectionX;
			vertices[3 * i + 1] = radius * currentDirectionY;
			vertices[3 * i + 2] = currentZ;

			indices[i] = i;
			i++;

			vertices[3 * i + 0] = nextRadius * nextDirectionX;
			vertices[3 * i + 1] = nextRadius * nextDirectionY;
			vertices[3 * i + 2] = nextZ;

			indices[i] = i;
			i++;

			vertices[3 * i + 0] = nextRadius * currentDirectionX;
			vertices[3 * i + 1] = nextRadius * currentDirectionY;
			vertices[3 * i + 2] = nextZ;

			indices[i] = i;
			i++;
		}
	}
  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];
  for(i=0;i<colorCount;i+=4){
    float r = 0.5+rand()*0.5/(RAND_MAX);
    colors[i]=R*r;
    colors[i+1]=G*r;
    colors[i+2]=B*r;
    colors[i+3]=1;
  }
  //udes to manipulate shade, didnt work as intended
  float* normals = new float[9*triangleCount];
  for(int i=0;i<triangleCount*9;i+=9){
    glm::vec3 node1 = glm::vec3(vertices[i],vertices[i+1],vertices[i+2]);
    glm::vec3 node2 = glm::vec3(vertices[i+3],vertices[i+4],vertices[i+5]);
    glm::vec3 node3 = glm::vec3(vertices[6],vertices[i+7],vertices[i+8]);

    glm::vec3 vector1 = node1-node2;
    glm::vec3 vector2 = node3-node2;
    glm::vec3 normal = (glm::cross(vector1,vector2));
    //printf("%.2f,%.2f,%.2f \n",normal.x,normal.z,normal.z);
    for(int k=0;k<9;k+=3){
      normals[i+k+0]=normal.x;
      normals[i+k+1]=normal.z;
      normals[i+k+2]=normal.z;
    }
  }
	unsigned int vao_id = setupVAO(vertices,indices,colors,normals,triangleCount);

	// Cleaning up after ourselves
	delete[] vertices;
	delete[] indices;
  delete[] colors;

	return vao_id;
}

unsigned int createBoardVAO(unsigned int box_x, unsigned int box_z, unsigned int n_boxes_x, unsigned int n_boxes_z){
	const unsigned int PRIMITIVES_PER_RECTANGLE = 2;
	const unsigned int triangleCount = n_boxes_x*n_boxes_z* PRIMITIVES_PER_RECTANGLE;

	// Allocating buffers
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];
  int i = 0;
  for(int current_x=0;current_x<n_boxes_x;current_x++){
    for(int current_z=0;current_z<n_boxes_z;current_z++){
      //triangle one
      vertices[3 * i + 0]=current_x*box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z;
      indices[i]=i;
      i++;

      vertices[3 * i + 0]=current_x*box_x+box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z;
      indices[i]=i;
      i++;

      vertices[3 * i + 0]=current_x*box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z+box_z;
      indices[i]=i;
      i++;

      //triangle two
      vertices[3 * i + 0]=current_x*box_x+box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z;
      indices[i]=i;
      i++;

      vertices[3 * i + 0]=current_x*box_x+box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z+box_z;
      indices[i]=i;
      i++;

      vertices[3 * i + 0]=current_x*box_x;
      vertices[3 * i + 1]=0;
      vertices[3 * i + 2]=current_z*box_z+box_z;
      indices[i]=i;
      i++;
    }
  }
  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];
  int j;
  float r;
  for(i=0;i<triangleCount;i+=4){
    for(j=i;j<i+6;j++){
      //colors first rectangle
      r = 0.8+rand()*0.2/(RAND_MAX);
      colors[i]=1*r;
      colors[i+1]=0.2*r;
      colors[i+2]=0.2*r;
      colors[i+3]=1;
    }
    for(j=i+6;j<i+12;j++){
      //colors first rectangle
      r = 0.8+rand()*0.2/(RAND_MAX);
      colors[i]=0*r;
      colors[i+1]=0.2*r;
      colors[i+2]=0.2*r;
      colors[i+3]=1;
    }

  }
  //udes to manipulate shade, didnt work as intended
  float* normals = new float[9*triangleCount];

  for(i=0;i<triangleCount*9;i+=9){
    glm::vec3 node1 = glm::vec3(vertices[i],vertices[i+1],vertices[i+2]);
    glm::vec3 node2 = glm::vec3(vertices[i+3],vertices[i+4],vertices[i+5]);
    glm::vec3 node3 = glm::vec3(vertices[6],vertices[i+7],vertices[i+8]);

    glm::vec3 vector1 = node1-node2;
    glm::vec3 vector2 = node3-node2;
    glm::vec3 normal = (glm::cross(vector1,vector2));
    //printf("%.2f,%.2f,%.2f \n",normal.x,normal.z,normal.z);
    for(j=0;j<9;j+=3){
      normals[i+j+0]=normal.x;
      normals[i+j+1]=normal.z;
      normals[i+j+2]=normal.z;
    }
  }
	unsigned int vao_id = setupVAO(vertices,indices,colors,normals,triangleCount);

	// Cleaning up after ourselves
	delete[] vertices;
	delete[] indices;
  delete[] colors;

	return vao_id;
} 

unsigned int createSquareVAO2(unsigned int box_x, unsigned int box_z, float R, float G, float B){
	const unsigned int triangleCount = 2;

	// Allocating buffers
	const unsigned int VERTICES_PER_TRIANGLE = 3;
	const unsigned int COMPONENTS_PER_VERTEX = 3;
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];
  //vertex1
  int i=0;
  vertices[0]=0;
  vertices[1]=0;
  vertices[2]=0;
  indices[i]=i;
  i++;

  vertices[3]=box_x;
  vertices[4]=0;
  vertices[5]=0;
  indices[i]=i;
  i++;

  
  vertices[6]=0;
  vertices[7]=0;
  vertices[8]=box_z;
  indices[i]=i;
  i++;

  vertices[9]=box_x;
  vertices[10]=0;
  vertices[11]=0;
  indices[i]=i;
  i++;

  vertices[12]=box_x;
  vertices[13]=0;
  vertices[12]=box_z;
  indices[i]=i;
  i++;

  vertices[15]=0;
  vertices[16]=0;
  vertices[17]=box_z;
  indices[i]=i;
  i++;


  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];
  int j;

  for(i=0;i<colorCount;i+=4){
    float r = 0.5+rand()*0.5/(RAND_MAX);
    colors[i]=R*r;
    colors[i+1]=G*r;
    colors[i+2]=B*r;
    colors[i+3]=1;
  }
  //udes to manipulate shade, didnt work as intended
  //
  float* normals = new float[9*triangleCount];
  for(i=0;i<triangleCount*9;i+=9){
    glm::vec3 node1 = glm::vec3(vertices[i],vertices[i+1],vertices[i+2]);
    glm::vec3 node2 = glm::vec3(vertices[i+3],vertices[i+4],vertices[i+5]);
    glm::vec3 node3 = glm::vec3(vertices[6],vertices[i+7],vertices[i+8]);

    glm::vec3 vector1 = node1-node2;
    glm::vec3 vector2 = node3-node2;
    glm::vec3 normal = (glm::cross(vector1,vector2));
    //printf("%.2f,%.2f,%.2f \n",normal.x,normal.z,normal.z);
    for(j=0;j<9;j+=3){
      normals[i+j+0]=normal.x;
      normals[i+j+1]=normal.z;
      normals[i+j+2]=normal.z;
    }
  }
	unsigned int vao_id = setupVAO(vertices,indices,colors,normals,triangleCount);

	// Cleaning up after ourselves
	delete[] vertices;
	delete[] indices;
  delete[] colors;

	return vao_id;
} 

unsigned int createSquareVAO(unsigned int box_x, unsigned int box_z, float R, float G, float B){
	const unsigned int triangleCount = 2;

	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];

  int i=0;

  vertices[3 * i + 0 ]=0;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=0;
  i++;
  vertices[3 * i + 0 ]=1;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=0;
  i++;
  vertices[3 * i + 0 ]=0;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=-1;
  i++;
  vertices[3 * i + 0 ]=1;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=0;
  i++;
  vertices[3 * i + 0 ]=1;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=-1;
  i++;

  vertices[3 * i + 0 ]=0;
  vertices[3 * i + 1 ]=0;
  vertices[3 * i + 2 ]=-1;
  i++;
  
  return createVAO(vertices,triangleCount,R,G,B);
}
float* buildTriangle2D(glm::vec3 vec_a, glm::vec3 vec_b, glm::vec3 vec_c,float y){
  glm::vec3 vec_A = {vec_a.x,y,vec_a.z};
  glm::vec3 vec_B = {vec_b.x,y,vec_b.z};
  glm::vec3 vec_C = {vec_c.x,y,vec_c.z};
  float* triangles = new float[8*3*3];

  glm::vec3 vertex_list[8*3] = {
    vec_a,vec_b,vec_c,
    vec_A,vec_B,vec_C,
    vec_a,vec_b,vec_B,
    vec_B,vec_A,vec_a,
    vec_b,vec_c,vec_C,
    vec_C,vec_B,vec_b,
    vec_c,vec_a,vec_A,
    vec_A,vec_C,vec_c
  };
  int i;
  for(i=0;i<8*3;i++){
    triangles[3 * i + 0 ]=vertex_list[i].x;
    triangles[3 * i + 1 ]=vertex_list[i].y;
    triangles[3 * i + 2 ]=vertex_list[i].z;
  }
  return triangles;
}

unsigned int createHexagonVAO(float R, float G, float B){
  const unsigned int num_obj=6;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;
  int curr=0;

  glm::vec3 vec_a(-0.6,0,1); //vertex x, lower position
  glm::vec3 vec_b(0.6,0,1);
  glm::vec3 vec_c(0,0,0);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }

  vec_a= vec_b;
  vec_b={1,0,0};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={0.6,0,-1};
  float* triangle3 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle3[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-0.6,0,-1};
  float* triangle4 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle4[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-1,0,0};
  float* triangle5 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle5[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-0.6,0,1};
  float* triangle6 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle6[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
}
unsigned int createPacmanVAO(float R, float G, float B){
  const unsigned int num_obj=9;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];
  float t1 = 0.5;
  float t2 = 0.86;
  int i;
  int current_index;
  int curr=0;

  glm::vec3 vec_a(0,0,1); //vertex x, lower position
  glm::vec3 vec_b(t1,0,t2);
  glm::vec3 vec_c(0,0,0);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={t2,0,t1};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={1,0,0};
  float* triangle3 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle3[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={t2,0,-t1};
  float* triangle4 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle4[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={t1,0,-t2};
  float* triangle5 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle5[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={0,0,-1};
  float* triangle6 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle6[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-t1,0,-t2};
  float* triangle7 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle7[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-t2,0,-t1};
  float* triangle8 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle8[i];
    curr++;
  }
  vec_a= vec_b;
  vec_b={-1,0,0};
  float* triangle9 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle9[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
}

unsigned int createBoxVAO(float R, float G, float B){
  const unsigned int num_obj=2;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;

  glm::vec3 vec_a(-1,0,1); //vertex x, lower position
  glm::vec3 vec_b(1,0,1);
  glm::vec3 vec_c(-1,0,-1);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);

  vec_a={1,0,1};
  vec_b={1,0,-1};
  vec_c={-1,0,-1};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,0.999);
  
  int curr=0;
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
} 
unsigned int createParallelogramVAO(float R, float G, float B){
  const unsigned int num_obj=2;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;
  float l = 0.7;

  glm::vec3 vec_a(-1,0,1); //vertex x, lower position
  glm::vec3 vec_b(l,0,1);
  glm::vec3 vec_c(-l,0,-1);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);

  vec_a={l,0,1};
  vec_b={1,0,-1};
  vec_c={-l,0,-1};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,0.999);
  
  int curr=0;
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
} 

unsigned int createStandardTriangleVAO(float R, float G, float B){
  const unsigned int num_obj=1;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;
  int curr=0;
  float t1 = 0.5;
  float t2 = 0.86;

  glm::vec3 vec_a(-t2,0,t1); //vertex x, lower position
  glm::vec3 vec_b(t2,0,t1);
  glm::vec3 vec_c(0,0,-t2);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
} 
unsigned int createWeirdTriangleVAO(float R, float G, float B){
  const unsigned int num_obj=4;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;
  int curr=0;

  glm::vec3 vec_a(-1,0,1); //vertex x, lower position
  glm::vec3 vec_b(-0.7,0,1);
  glm::vec3 vec_c(0,0,-1);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }

  vec_a={-0.7,0,1};
  vec_b={0,0,-0.7};
  vec_c={0,0,-1};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
  vec_a={1,0,1};
  vec_b={0,0,-1};
  vec_c={0.7,0,1};
  float* triangle3 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle3[i];
    curr++;
  }
  vec_a={0.7,0,1};
  vec_b={0,0,-1};
  vec_c={0,0,-0.7};
  float* triangle4 = buildTriangle2D(vec_a,vec_b,vec_c,1);
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle4[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
} 
unsigned int createStarVAO(float R, float G, float B){
  const unsigned int num_obj=2;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	float* vertices = new float[num_obj*vertices_per_obj];

  int i;
  int current_index;

  glm::vec3 vec_a(-1,0,0.5); //vertex x, lower position
  glm::vec3 vec_b(1,0,0.5);
  glm::vec3 vec_c(0,0,-1);
  float* triangle1 = buildTriangle2D(vec_a,vec_b,vec_c,1);

  vec_a={0,0,1};
  vec_b={1,0,-0.5};
  vec_c={-1,0,-0.5};
  float* triangle2 = buildTriangle2D(vec_a,vec_b,vec_c,0.999);
  
  int curr=0;
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle1[i];
    curr++;
  }
  for(i=0;i<vertices_per_obj;i++){
    vertices[curr]=triangle2[i];
    curr++;
  }
	return createVAO(vertices,triangleCount,R,G,B);
} 

unsigned int createVAO(float* vertices, int triangleCount, float R, float G, float B){
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];
  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];
  float* normals = new float[9*triangleCount];

  for(i=0;i<triangleCount*VERTICES_PER_TRIANGLE;i++){
    indices[i]=i;
  }


  for(i=0;i<colorCount;i+=4){
    colors[i]=R;
    colors[i+1]=G;
    colors[i+2]=B;
    colors[i+3]=1;
  }
  int j;
  for(i=0;i<triangleCount*9;i+=9){
    glm::vec3 node1 = glm::vec3(vertices[i],vertices[i+1],vertices[i+2]);
    glm::vec3 node2 = glm::vec3(vertices[i+3],vertices[i+4],vertices[i+5]);
    glm::vec3 node3 = glm::vec3(vertices[6],vertices[i+7],vertices[i+8]);

    glm::vec3 vector1 = node1-node2;
    glm::vec3 vector2 = node3-node2;
    glm::vec3 normal = (glm::cross(vector1,vector2));
    //printf("%.2f,%.2f,%.2f \n",normal.x,normal.z,normal.z);
    for(j=0;j<9;j+=3){
      normals[i+j+0]=normal.x;
      normals[i+j+1]=normal.z;
      normals[i+j+2]=normal.z;
    }
  }
	unsigned int vao_id = setupVAO(vertices,indices,colors,normals,triangleCount);

	// Cleaning up after ourselves
	delete[] vertices;
	delete[] indices;
  delete[] colors;

  return vao_id;
}

