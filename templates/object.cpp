/*
* Copyright (c) 2015-18 Luke Montalvo <lukemontalvo@gmail.com>
*
* This file is part of BEE.
* BEE is free software and comes with ABSOLUTELY NO WARANTY.
* See LICENSE for more details.
*/

// BEEF auto-generated the below code and will overwrite all changes

#ifndef RES_{capname}
#define RES_{capname} 1

#include "../../bee/util.hpp"
#include "../../bee/all.hpp"

#include "../resources.hpp"

#include "{name}.hpp"

{headers}

{objname}::{objname}() : Object("{name}", "{name}.cpp") {{
	implemented_events.insert({{
		{implevents}
	}});
	{is_persistent}
}}

{events}

#endif // RES_{capname}
