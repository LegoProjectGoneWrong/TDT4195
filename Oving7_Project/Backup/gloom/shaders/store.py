float* buildFigure(float* nodes, int num_obj){
	const unsigned int VERTICES_PER_TRIANGLE = 3;
	const unsigned int COMPONENTS_PER_VERTEX = 3;
	const unsigned int triangles_per_obj = 8;
  const unsigned int vertices_per_obj = triangles_per_obj* VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	// Allocating buffers
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];

  
  int k;
  int i;
  for(i=0;i<9*num_obj;i+=9){
    printf("triangle %d\n",i);
    glm::vec3 vec_a = {nodes[i+0],nodes[i+1],nodes[i+2]};
    glm::vec3 vec_b = {nodes[i+3],nodes[i+4],nodes[i+5]};
    glm::vec3 vec_c = {nodes[i+6],nodes[i+7],nodes[i+8]};
    float* triangles= buildTriangle2D(vec_a,vec_b,vec_c);

    printf("%.2f,%.2f,%.2f \n",nodes[i+0],nodes[i+1],nodes[i+2]);

    for(k=0;k<vertices_per_obj;k++){
      vertices[k]=triangles[k];
      printf("%.2f\n",float(triangles[k]));
    }
  }
  return vertices;
}

unsigned int createStarVAO3(float R, float G, float B){
	const unsigned int VERTICES_PER_TRIANGLE = 3;
	const unsigned int COMPONENTS_PER_VERTEX = 3;
	const unsigned int triangles_per_obj = 8;

  const unsigned int num_obj = 2;
  const unsigned int triangleCount = num_obj*triangles_per_obj;

	// Allocating buffers
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];


  float nodes[num_obj*9]={
    0,0,0.5,
    1,0,0.5,
    0,0,-0.5,
    0,0,-0.3,
    1,0,-0.5,
    -1,0,-0.5
  };
  vertices =  buildFigure(nodes,num_obj);
  int i;
  for(i=0;i<triangleCount*VERTICES_PER_TRIANGLE;i++){
    indices[i]=i;
  }


  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];


  for(i=0;i<colorCount;i+=4){
    colors[i]=R;
    colors[i+1]=G;
    colors[i+2]=B;
    colors[i+3]=1;
  }
  int j;
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

unsigned int createStarVAO2(float R, float G, float B){
	const unsigned int triangleCount = 8;

	// Allocating buffers
	const unsigned int VERTICES_PER_TRIANGLE = 3;
	const unsigned int COMPONENTS_PER_VERTEX = 3;
	float* vertices = new float[triangleCount * VERTICES_PER_TRIANGLE * COMPONENTS_PER_VERTEX];
	unsigned int* indices = new unsigned int[triangleCount * VERTICES_PER_TRIANGLE];

  glm::vec3 nx(-1,0,0.5); //vertex x, lower position
  glm::vec3 nX(-1,1,0.5); //vertex x, upper position
  glm::vec3 ny(1,0,0.5);
  glm::vec3 nY(1,1,0.5);
  glm::vec3 nz(0,0,-1);
  glm::vec3 nZ(0,1,-1);

  glm::vec3 vertex_list[triangleCount*3] = {
    nx,ny,nz,
    nX,nY,nZ,
    nx,ny,nY,
    nY,nX,nx,
    ny,nz,nZ,
    nZ,nY,ny,
    nz,nx,nX,
    nX,nZ,nz
  };
  int i;
  for(i=0;i<triangleCount*3;i++){
    vertices[3 * i + 0 ]=vertex_list[i].x;
    vertices[3 * i + 1 ]=vertex_list[i].y;
    vertices[3 * i + 2 ]=vertex_list[i].z;
    indices[i]=i;
  }

  int colorCount = triangleCount*3*4;
  float* colors = new float[colorCount];

  for(i=0;i<colorCount;i+=4){
    colors[i]=R;
    colors[i+1]=G;
    colors[i+2]=B;
    colors[i+3]=1;
  }
  int j;
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

