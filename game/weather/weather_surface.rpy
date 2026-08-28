## Ground-impact, ripple, wet-reflection and roof-drip passes. They only add
## faint transparent marks; no pass samples or warps the background texture.

init python:
    renpy.register_shader(
        "longzu.weather.surface",
        variables="""
            uniform float u_weather_rain_strength;
            uniform float u_weather_sunset_strength;
            uniform float u_weather_ground_mask_enabled;
            uniform sampler2D u_weather_ground_mask;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_surface_uv;
        """,
        vertex_300="""
            v_weather_surface_uv = a_position.xy / u_model_size;
        """,
        fragment_functions="""
            float weather_surface_hash(vec2 value) {
                return fract(sin(dot(value, vec2(71.3, 193.9))) * 28713.4241);
            }

            float weather_surface_ring(vec2 uv, vec2 grid, float weather_time, float scale, float seed) {
                vec2 cell = floor(uv * grid);
                vec2 local = fract(uv * grid) - 0.5;
                float variation = weather_surface_hash(cell + seed);
                float phase = fract(weather_time * (0.48 + variation * 0.72) + variation * 31.7);
                float active = 1.0 - step(0.62, phase);
                float radius = (0.045 + phase * 0.31) * (0.70 + variation * 0.55) * scale;
                vec2 ellipse = vec2(local.x * 0.66, local.y * 2.25);
                float ring = 1.0 - smoothstep(0.014, 0.034, abs(length(ellipse) - radius));
                float fade = (1.0 - phase / 0.62);
                return ring * active * fade;
            }
        """,
        fragment_400="""
            float ground_sample = texture2D(u_weather_ground_mask, v_weather_surface_uv).r;
            float ground_fallback = smoothstep(0.46, 0.61, v_weather_surface_uv.y);
            float ground = mix(ground_fallback, ground_sample, u_weather_ground_mask_enabled);
            float weather_time = u_time;
            float rain = clamp(u_weather_rain_strength, 0.0, 1.0);
            float sunset = clamp(u_weather_sunset_strength, 0.0, 1.0);

            float ripples = weather_surface_ring(v_weather_surface_uv, vec2(15.0, 7.0), weather_time, 1.00, 4.0);
            ripples += weather_surface_ring(v_weather_surface_uv + vec2(0.123, 0.047), vec2(10.0, 5.0), weather_time, 1.36, 28.0) * 0.72;

            vec2 impact_cell = floor(v_weather_surface_uv * vec2(26.0, 12.0));
            vec2 impact_local = fract(v_weather_surface_uv * vec2(26.0, 12.0)) - 0.5;
            float impact_seed = weather_surface_hash(impact_cell + 64.0);
            float impact_phase = fract(weather_time * (1.90 + impact_seed * 1.80) + impact_seed * 83.0);
            float impact_active = 1.0 - step(0.14 + rain * 0.32, impact_phase);
            vec2 impact_ellipse = vec2(impact_local.x * 0.82, impact_local.y * 2.90);
            float impact_dot = 1.0 - smoothstep(0.025, 0.095, length(impact_ellipse));
            float splash = impact_dot * impact_active * (0.16 + rain * 0.84);

            float shimmer = sin(v_weather_surface_uv.x * 82.0 + weather_time * 0.47 + v_weather_surface_uv.y * 19.0);
            shimmer = smoothstep(0.74, 0.97, shimmer) * (0.010 + 0.028 * sunset + 0.014 * rain);

            float alpha = ground * (ripples * rain * 0.15 + splash * 0.12 + shimmer);
            vec3 wet_color = mix(vec3(0.61, 0.74, 0.84), vec3(1.0, 0.67, 0.33), sunset * 0.72);
            gl_FragColor = vec4(wet_color * alpha, alpha);
        """,
    )

    renpy.register_shader(
        "longzu.weather.roof_drips",
        variables="""
            uniform float u_weather_roof_drip_strength;
            uniform float u_weather_roof_mask_enabled;
            uniform sampler2D u_weather_roof_mask;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_roof_uv;
        """,
        vertex_300="""
            v_weather_roof_uv = a_position.xy / u_model_size;
        """,
        fragment_400="""
            float roof_here = texture2D(u_weather_roof_mask, v_weather_roof_uv).r;
            float roof_above = texture2D(u_weather_roof_mask, v_weather_roof_uv - vec2(0.0, 0.008)).r;
            float roof_shift_a = texture2D(u_weather_roof_mask, v_weather_roof_uv - vec2(0.0, 0.030)).r;
            float roof_shift_b = texture2D(u_weather_roof_mask, v_weather_roof_uv - vec2(0.0, 0.057)).r;
            float roof_shift_c = texture2D(u_weather_roof_mask, v_weather_roof_uv - vec2(0.0, 0.089)).r;
            float roof_edge = roof_above * (1.0 - roof_here);
            roof_edge = max(roof_edge, roof_shift_a * (1.0 - roof_here));
            roof_edge = max(roof_edge, roof_shift_b * (1.0 - roof_here));
            roof_edge = max(roof_edge, roof_shift_c * (1.0 - roof_here));
            float fallback_edge = 1.0 - smoothstep(0.235, 0.257, v_weather_roof_uv.y);
            roof_edge = mix(fallback_edge, roof_edge, u_weather_roof_mask_enabled);

            float roof_time = u_time;
            float column = floor(v_weather_roof_uv.x * 94.0);
            float seed = fract(sin(column * 71.77) * 39173.71);
            float phase = fract(roof_time * (0.52 + seed * 0.58) + seed * 19.0);
            float available = step(1.0 - clamp(u_weather_roof_drip_strength, 0.0, 1.0), seed);
            float thin_line = 1.0 - smoothstep(0.025, 0.072, abs(fract(v_weather_roof_uv.x * 94.0) - 0.5));
            float pulse = smoothstep(0.12, 0.38, phase) * (1.0 - smoothstep(0.82, 1.0, phase));
            float alpha = roof_edge * thin_line * available * pulse * (0.12 + u_weather_roof_drip_strength * 0.36);
            vec3 drip_color = vec3(0.62, 0.75, 0.84);
            gl_FragColor = vec4(drip_color * alpha, alpha);
        """,
    )

    def weather_apply_surface_uniforms(trans, st, at):
        params = weather_params()
        ground_mask, ground_enabled = weather_mask_payload("ground")
        trans.u_weather_rain_strength = params["rain_strength"]
        trans.u_weather_sunset_strength = params["sunset_strength"]
        trans.u_weather_ground_mask = ground_mask
        trans.u_weather_ground_mask_enabled = ground_enabled
        return 0.0

    def weather_apply_roof_uniforms(trans, st, at):
        params = weather_params()
        roof_mask, roof_enabled = weather_mask_payload("roof")
        trans.u_weather_roof_mask = roof_mask
        trans.u_weather_roof_mask_enabled = roof_enabled
        trans.u_weather_roof_drip_strength = min(
            1.0,
            params["rain_strength"] + params["rain_fog_strength"] * 0.24,
        )
        return 0.0

transform weather_surface_pass:
    shader "longzu.weather.surface"
    function weather_apply_surface_uniforms

transform weather_roof_drip_pass:
    shader "longzu.weather.roof_drips"
    function weather_apply_roof_uniforms

screen weather_surface_layer():
    fixed:
        xfill True
        yfill True
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_surface_pass
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_roof_drip_pass
