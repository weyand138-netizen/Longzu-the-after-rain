## Atmosphere and spatial sunset lighting. These are transparent overlays: the
## background image remains one unmodified, fixed displayable underneath them.

init python:
    renpy.register_shader(
        "longzu.weather.cloud_grade",
        variables="""
            uniform float u_weather_cloud_darkness;
            uniform float u_weather_sky_mask_enabled;
            uniform sampler2D u_weather_sky_mask;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_atmo_uv;
        """,
        vertex_300="""
            v_weather_atmo_uv = a_position.xy / u_model_size;
        """,
        fragment_400="""
            float sky_sample = texture2D(u_weather_sky_mask, v_weather_atmo_uv).r;
            float sky_fallback = 1.0 - smoothstep(0.42, 0.88, v_weather_atmo_uv.y);
            float sky = mix(sky_fallback, sky_sample, u_weather_sky_mask_enabled);
            float cloud = clamp(u_weather_cloud_darkness, 0.0, 1.0);
            // Wide, low-contrast cloud banks move across the overlay only.
            // The long, mismatched periods prevent a visible loop or a
            // screen-wide breathing effect while making overcast feel alive.
            float cloud_time = u_time;
            float bank_a = sin(v_weather_atmo_uv.x * 5.4 + v_weather_atmo_uv.y * 2.1 - cloud_time * 0.075);
            float bank_b = sin(v_weather_atmo_uv.x * 2.0 - v_weather_atmo_uv.y * 6.8 - cloud_time * 0.031 + 1.8);
            float cloud_drift = clamp(0.89 + bank_a * 0.09 + bank_b * 0.06, 0.76, 1.04);
            float alpha = cloud * (0.10 + 0.33 * sky + 0.10 * (1.0 - v_weather_atmo_uv.y)) * cloud_drift;
            vec3 cloud_color = mix(vec3(0.08, 0.12, 0.17), vec3(0.18, 0.24, 0.30), sky);
            gl_FragColor = vec4(cloud_color * alpha, alpha);
        """,
    )

    renpy.register_shader(
        "longzu.weather.haze",
        variables="""
            uniform float u_weather_rain_fog_strength;
            uniform float u_weather_distance_mask_enabled;
            uniform sampler2D u_weather_distance_mask;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_haze_uv;
        """,
        vertex_300="""
            v_weather_haze_uv = a_position.xy / u_model_size;
        """,
        fragment_400="""
            float distance_sample = texture2D(u_weather_distance_mask, v_weather_haze_uv).r;
            float horizon_band = exp(-pow((v_weather_haze_uv.y - 0.47) / 0.24, 2.0));
            float distance_fallback = max(horizon_band, 1.0 - smoothstep(0.16, 0.52, v_weather_haze_uv.y));
            float distance_mask = mix(distance_fallback, distance_sample, u_weather_distance_mask_enabled);
            float fog = clamp(u_weather_rain_fog_strength, 0.0, 1.0);
            float alpha = fog * distance_mask * (0.035 + 0.19 * horizon_band);
            vec3 haze_color = vec3(0.47, 0.58, 0.66);
            gl_FragColor = vec4(haze_color * alpha, alpha);
        """,
    )

    renpy.register_shader(
        "longzu.weather.sunset",
        variables="""
            uniform float u_weather_sunset_strength;
            uniform float u_weather_cloud_darkness;
            uniform float u_weather_sky_mask_enabled;
            uniform sampler2D u_weather_sky_mask;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_sunset_uv;
        """,
        vertex_300="""
            v_weather_sunset_uv = a_position.xy / u_model_size;
        """,
        fragment_400="""
            float sky_sample = texture2D(u_weather_sky_mask, v_weather_sunset_uv).r;
            float sky_fallback = 1.0 - smoothstep(0.46, 0.90, v_weather_sunset_uv.y);
            float sky = mix(sky_fallback, sky_sample, u_weather_sky_mask_enabled);
            float horizon = exp(-pow((v_weather_sunset_uv.y - 0.46) / 0.135, 2.0));
            float sunset_time = u_time;
            // Two long, low-amplitude waves emulate thin clouds crossing the
            // sun. Their combined 10–29s rhythm stays below visible "breathing".
            float sun_variation = 0.975
                + sin(sunset_time * 0.29 + 0.6) * 0.018
                + sin(sunset_time * 0.071 + 2.1) * 0.012;
            float sunset = clamp(u_weather_sunset_strength, 0.0, 1.0) * sun_variation;
            float unblocked = 1.0 - clamp(u_weather_cloud_darkness, 0.0, 1.0) * 0.78;
            float alpha = sunset * unblocked * sky * horizon * 0.19;
            vec3 amber = mix(vec3(0.90, 0.47, 0.19), vec3(1.0, 0.73, 0.38), horizon);
            gl_FragColor = vec4(amber * alpha, alpha);
        """,
    )

    renpy.register_shader(
        "longzu.weather.godrays",
        variables="""
            uniform float u_weather_godray_strength;
            uniform float u_weather_cloud_darkness;
            uniform float u_weather_sky_mask_enabled;
            uniform sampler2D u_weather_sky_mask;
            uniform float u_time;
            uniform vec2 u_model_size;
            attribute vec4 a_position;
            varying vec2 v_weather_ray_uv;
        """,
        vertex_300="""
            v_weather_ray_uv = a_position.xy / u_model_size;
        """,
        fragment_400="""
            float sky_sample = texture2D(u_weather_sky_mask, v_weather_ray_uv).r;
            float sky_fallback = 1.0 - smoothstep(0.44, 0.86, v_weather_ray_uv.y);
            float sky = mix(sky_fallback, sky_sample, u_weather_sky_mask_enabled);
            float ray_time = u_time;
            float height = max(0.0, 0.52 - v_weather_ray_uv.y);
            float drift_a = sin(ray_time * 0.20) * 0.010;
            float drift_b = sin(ray_time * 0.13 + 1.7) * 0.014;
            float beam_a = exp(-pow((v_weather_ray_uv.x - 0.66 - height * 0.36 - drift_a) / 0.105, 2.0));
            float beam_b = exp(-pow((v_weather_ray_uv.x - 0.72 - height * 0.12 + drift_b) / 0.065, 2.0));
            float beam_c = exp(-pow((v_weather_ray_uv.x - 0.59 + height * 0.19 - drift_a) / 0.045, 2.0));
            float beam_d = exp(-pow((v_weather_ray_uv.x - 0.78 - height * 0.57 + drift_b) / 0.082, 2.0));
            float cloud_shift = 0.76 + 0.18 * sin(ray_time * 0.17 + v_weather_ray_uv.x * 9.0);
            float rays = (beam_a * 0.60 + beam_b * 0.42 + beam_c * 0.26 + beam_d * 0.36);
            float alpha = clamp(u_weather_godray_strength, 0.0, 1.0)
                * (1.0 - clamp(u_weather_cloud_darkness, 0.0, 1.0))
                * sky * smoothstep(0.00, 0.11, height) * cloud_shift * rays * 0.070;
            vec3 ray_color = vec3(1.0, 0.73, 0.42);
            gl_FragColor = vec4(ray_color * alpha, alpha);
        """,
    )

    def weather_apply_atmosphere_uniforms(trans, st, at):
        params = weather_params()
        sky_mask, sky_enabled = weather_mask_payload("sky")
        trans.u_weather_cloud_darkness = params["cloud_darkness"]
        trans.u_weather_rain_fog_strength = params["rain_fog_strength"]
        trans.u_weather_sunset_strength = params["sunset_strength"]
        trans.u_weather_godray_strength = params["godray_strength"]
        trans.u_weather_sky_mask = sky_mask
        trans.u_weather_sky_mask_enabled = sky_enabled
        return 0.0

    def weather_apply_haze_uniforms(trans, st, at):
        params = weather_params()
        distance_mask, distance_enabled = weather_mask_payload("distance")
        trans.u_weather_rain_fog_strength = params["rain_fog_strength"]
        trans.u_weather_distance_mask = distance_mask
        trans.u_weather_distance_mask_enabled = distance_enabled
        return 0.0

transform weather_cloud_grade_pass:
    shader "longzu.weather.cloud_grade"
    function weather_apply_atmosphere_uniforms

transform weather_haze_pass:
    shader "longzu.weather.haze"
    function weather_apply_haze_uniforms

transform weather_sunset_pass:
    shader "longzu.weather.sunset"
    function weather_apply_atmosphere_uniforms
    blend "add"

transform weather_godray_pass:
    shader "longzu.weather.godrays"
    function weather_apply_atmosphere_uniforms
    blend "add"

screen weather_atmosphere_layer():
    fixed:
        xfill True
        yfill True
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_cloud_grade_pass
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_haze_pass
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_sunset_pass
        add Solid("#ffffff"):
            xsize config.screen_width
            ysize config.screen_height
            at weather_godray_pass
