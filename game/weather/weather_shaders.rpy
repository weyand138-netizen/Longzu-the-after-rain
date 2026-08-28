## GPU rain pass. A single fullscreen model produces all rain depths, so the
## fixed pool lives in the shader rather than allocating per-frame objects.

init python:
    renpy.register_shader(
        "longzu.weather.rain",
        variables="""
            uniform float u_weather_rain_strength;
            uniform float u_weather_wind;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_uv;
        """,
        vertex_300="""
            v_weather_uv = a_position.xy / u_model_size;
        """,
        fragment_functions="""
            float weather_hash(vec2 value) {
                return fract(sin(dot(value, vec2(127.1, 311.7))) * 43758.5453123);
            }

            float weather_rain_band(
                vec2 uv,
                float columns,
                float rows,
                float speed,
                float length,
                float width,
                float density,
                float wind,
                float seed,
                float weather_time
            ) {
                vec2 grid = vec2(columns, rows);
                vec2 moving = uv * grid;
                moving.y -= weather_time * speed;

                vec2 cell = floor(moving);
                vec2 local = fract(moving);
                float exists = step(1.0 - density, weather_hash(cell + seed));
                float x_jitter = weather_hash(vec2(cell.x, seed)) - 0.5;
                float slanted_x = local.x - 0.5 - x_jitter * 0.36 - wind * (local.y - 0.5);
                float strand = 1.0 - smoothstep(width, width * 2.2, abs(slanted_x));
                float tail = smoothstep(1.0 - length, 1.0 - length * 0.22, local.y);
                return exists * strand * tail;
            }
        """,
        fragment_400="""
            float strength = clamp(u_weather_rain_strength, 0.0, 1.0);
            float wind = clamp(u_weather_wind, -1.0, 1.0) * 0.36;
            float weather_time = u_time;

            // Far: 32 x 18 x 0.80 ~= 460 candidate drops, thin and slow.
            float far_rain = weather_rain_band(
                v_weather_uv, 32.0, 18.0, 1.35, 0.30, 0.026,
                0.18 + strength * 0.66, wind * 0.45, 7.0, weather_time
            );
            // Mid: 24 x 12 x 0.82 ~= 236 candidate drops.
            float mid_rain = weather_rain_band(
                v_weather_uv, 24.0, 12.0, 2.35, 0.48, 0.042,
                max(0.0, strength - 0.08) * 0.90, wind * 0.74, 19.0, weather_time
            );
            // Foreground: 12 x 8 x 0.80 ~= 77 candidate drops, long and bright.
            float near_rain = weather_rain_band(
                v_weather_uv, 12.0, 8.0, 4.20, 0.72, 0.068,
                max(0.0, strength - 0.22) * 0.98, wind, 43.0, weather_time
            );

            vec3 rain_color = vec3(0.72, 0.84, 0.93);
            float rain_alpha = far_rain * 0.16 + mid_rain * 0.34 + near_rain * 0.50;
            gl_FragColor = vec4(rain_color * rain_alpha, rain_alpha);
        """,
    )

    def weather_apply_rain_uniforms(trans, st, at):
        params = weather_params()
        trans.u_weather_rain_strength = params["rain_strength"]
        trans.u_weather_wind = params["wind"]
        return 0.0

transform weather_rain_pass:
    shader "longzu.weather.rain"
    function weather_apply_rain_uniforms

screen weather_rain_layer():
    fixed:
        xfill True
        yfill True
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_rain_pass

screen weather_effects():
    fixed:
        id "weather_effects_root"
        xfill True
        yfill True
        use weather_atmosphere_layer
        use weather_surface_layer
        use weather_rain_layer

screen weather_scene_overlay():
    if weather_enabled and weather_motion_allowed():
        use weather_effects
