#version 430 core

layout(location=0) in vec3 position;

layout(location=1) in vec4 vertexColor;
out vec4 fragmentColor;
uniform layout(location = 2) float var;
uniform layout(location = 3) mat4x4 MVP;

void main()
{
      mat4 matrix;
      matrix[0][0] = matrix[1][1] = matrix[2][2] = matrix[3][3] = 1;
      matrix[3][1] = var;
      
      gl_Position = MVP*vec4(position,1.0f);
      fragmentColor = vertexColor;
}
