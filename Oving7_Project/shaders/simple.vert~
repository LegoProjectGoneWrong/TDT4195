#version 430 core

layout(location=0) in vec3 position;
layout(location=1) in vec4 vertexColor;
layout(location=2) in vec3 normals;

out vec4 fragmentColor;

uniform layout(location = 3) mat4x4 MVP;
uniform layout(location = 4) mat4x4 model;
uniform layout(location = 5) vec4 colorOverlay;
void main()
{
      vec4 pos = -vec4(position,0.0f);
      vec4 norm = vec4(normals,1.0f);
      float k = dot(normalize(model*norm),normalize(model*pos)); 
      gl_Position = MVP*vec4(position,1.0f);
      fragmentColor = vertexColor*max(k,0.5)+colorOverlay;
      fragmentColor[3]=1.0;
}
