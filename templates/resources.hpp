/*
* Copyright (c) 2015-18 Luke Montalvo <lukemontalvo@gmail.com>
*
* This file is part of BEE.
* BEE is free software and comes with ABSOLUTELY NO WARANTY.
* See LICENSE for more details.
*/

#ifndef RES_H
#define RES_H 1

#include "../bee/util.hpp"
#include "../bee/all.hpp"

#include "extras.hpp"

// BEEF auto-generated the below code and will overwrite all changes

// Define textures
extern bee::Texture* spr_none;

{textureDefines}

// Define sounds
{soundDefines}

// Define fonts
{fontDefines}

// Define paths
{pathDefines}

// Define timelines
{timelineDefines}

// Define meshes
{meshDefines}

// Define lights
{lightDefines}

// Define objects
{objectDefines}

// Define rooms
{roomDefines}

namespace bee {{
	int init_resources();
	int close_resources();
}}

#endif // RES_H
