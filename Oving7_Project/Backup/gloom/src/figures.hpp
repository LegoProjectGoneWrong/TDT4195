#ifndef FIGURES_H
#define FIGURES_H


#pragma once

#include <math.h>
#include "SceneGraph.hpp"
#include "program.hpp"

unsigned int createCircleVAO(unsigned int slices, unsigned int layers,float R, float G, float B);
unsigned int createBoardVAO(unsigned int box_x, unsigned int box_z, unsigned int n_boxes_x, unsigned int n_boxes_z);
unsigned int createSquareVAO(unsigned int box_x, unsigned int box_z, float R, float G, float B);
unsigned int createStarVAO(float R, float G, float B);
unsigned int createBoxVAO(float R, float G, float B);
unsigned int createHexagonVAO(float R, float G, float B);
unsigned int createWeirdTriangleVAO(float R, float G, float B);
unsigned int createPacmanVAO(float R, float G, float B);
unsigned int createParallelogramVAO(float R, float G, float B);
unsigned int createStandardTriangleVAO(float R, float G, float B);


#endif
