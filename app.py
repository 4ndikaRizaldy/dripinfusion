from track import *
import tempfile
import cv2
import numpy as np
import torch
import streamlit as st
import os



if __name__ == '__main__':
    st.set_page_config(page_icon="👨‍⚕️", 
                       page_title="Drip Infusion Dashboard", 
                       layout = 'wide', 
                       initial_sidebar_state = 'auto')
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"]{
        background-image: url("https://archive.org/download/untitled-design_20231012/Untitled%20design.png");
        background-size: cover;
    }
    [data-testid="stSidebar"]{
        background-image: url("https://archive.org/download/medical-healthcare-blue-background-design_1017-26837/medical-healthcare-blue-background-design_1017-26837.jpg");
        background-size: cover;

    }
    [data-testid="stHeader"]{
        background-image: none;        
        background-size: cover;
        filter: blur(100px);
    }
    
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    main_title = """
            <div>
                <h1 style="color:white;
                text-align:center; 
                font-size:40px;
                margin-top:10px;">
                Monitoring Drip Infusion</h1>
            </div>
            """
    
    sub_title = """
                <div>
                    <h3 style="color:white;
                    text-align:center;
                    margin-top:1px;">
                    Dasboard </h3>
                </div>
                """
    line = """
            <div style="text-align: center;"><font size="4" color="white">___</font></div>
             """

    __,logo, title,__ = st.columns([2,2,6,2])
    with logo:
        st.image('assets/LOGO-UNRAM-1.png', width=150, use_column_width="never", caption="Universitas Mataram", output_format="auto")
    with title:
            st.markdown(main_title,
                        unsafe_allow_html=True)
            st.markdown(sub_title,
                        unsafe_allow_html=True)
    st.markdown(
    '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
    unsafe_allow_html=True
    )

    
    # Sidebar Setting
    st.sidebar.markdown("""
    <div style="display: flex; 
        justify-content: center;
        margin-bottom:-40px">
        <h3 style="text-align: center;">
        Upload a video</h3>
    </div>
    """, unsafe_allow_html=True)
    video_file_buffer = st.sidebar.file_uploader("", type=['mp4', 'mov', 'avi'])
    assigned_class_id = [0]
    names = ['tetesan']
    st.sidebar.markdown("""
    <div style="display: flex; 
        justify-content: center;
        margin-bottom:-40px">
        <h3 style="text-align: center;">
        Confidence</h3>
    </div>
    """, unsafe_allow_html=True)
    confidence = st.sidebar.slider("", min_value=0.0, max_value=1.0, value=0.50)
    st.sidebar.markdown("""
    <div style="display: flex; 
        justify-content: center;
        margin-bottom:-40px">
        <h4 style="text-align: center;">
        Line position</h4>
    </div>
    """, unsafe_allow_html=True)
    lines = st.sidebar.number_input('', min_value=0.00, max_value=1.00, value=0.461, step=0.001, format='%.3f')

    status = st.empty()

    #Result
    tetesan, timer, fps = st.columns(3)
    with tetesan:
        st.markdown('<div style="text-align: center; margin-top: 20px"><font size="4" color="white">TETESAN</font></div>', unsafe_allow_html=True)
        tetesan_text = st.markdown(line, unsafe_allow_html=True)
    
    with timer:
        st.markdown('<div style="text-align: center; margin-top: 20px"><font size="4" color="white">TIMER</font></div>', unsafe_allow_html=True)
        timer_text = st.markdown(line, unsafe_allow_html=True)

    with fps:
        st.markdown('<div style="text-align: center; margin-top: 20px"><font size="4" color="white">FPS</font></div>', unsafe_allow_html=True)
        fps_text = st.markdown(line, unsafe_allow_html=True)
        
 
    st.markdown(
    '<hr style="border: 1px solid #ffffff; margin: 20px 0;">',
    unsafe_allow_html=True
    )

    col1, __, col2 = st.columns([2,2,2])
    with col1:
        if video_file_buffer:
            st.markdown('<p style="text-align:center;">Input Video</p>', unsafe_allow_html=True)
            st.video(video_file_buffer)
            
            # save video from streamlit into "videos" folder for future detect
            with open(os.path.join('videos', video_file_buffer.name), 'wb') as f:
                f.write(video_file_buffer.getbuffer())
    st.markdown(
    '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
    unsafe_allow_html=True
    )

    if video_file_buffer is None:
        status.markdown('<div style="text-align: center;"><font size="4" color="yellow"> Status: Waiting for input </font></div>', unsafe_allow_html=True)
    else:
        status.markdown('<div style="text-align: center;"><font size= "4" color="green"> Status: Ready </font></div>', unsafe_allow_html=True)
        
    track_button = st.sidebar.button('START',type='primary', use_container_width=True)
    # Tambahkan tombol 'STOP'
    stop_button = st.sidebar.button('STOP', type='secondary', use_container_width=True)
    

    with col2:
        if track_button:
            if video_file_buffer is None:
                status.markdown('<div style="text-align: center;"><font size= "4" color="red"> Status: Please! upload a video first </font></div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="text-align:center;">Output Video</p>', unsafe_allow_html=True)
                stframe = st.empty()
                opt = parse_opt()
                reset()
                opt.conf_thres = confidence
                opt.source = f'videos/{video_file_buffer.name}'
                
                # Display the output video
                output_video_path = os.path.join('inference', 'output', video_file_buffer.name)  # Update this path accordingly
                if os.path.exists(output_video_path):
                    st.video(open(output_video_path, 'rb').read())
                status.markdown('<div style="text-align: center;"><font size="4" color="blue"> Status: Running </font></div>', unsafe_allow_html=True)
                with torch.no_grad():
                    detect(opt, stframe, tetesan_text, timer_text, lines,  fps_text, assigned_class_id)
                status.markdown('<div style="text-align: center;"><font size="4" color="green"> Status: Finished! </font></div>', unsafe_allow_html=True)
                if stop_button:
                    st.stop()
                    
    footer_style = """
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: #FAFAFA;
    text-align: center;
    padding: 5xpx;
    """

    st.markdown(
        """
        <footer style='{}'>
            © 2023, A. Rizaldy
        </footer>
        """.format(footer_style),
        unsafe_allow_html=True
    )