from track import *
import torch
import streamlit as st
import os
import sqlite3
import pandas as pd


if __name__ == "__main__":
    st.set_page_config(
        page_icon="👨‍⚕️",
        page_title="Drip Infusion Dashboard",
        layout="wide",
        initial_sidebar_state="auto",
    )
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
    [data-testid="st-emotion-cache-10pw50"]{
        filter: blur(100px);
        
    }
        MainMenu {visibility: hidden;}
        # footer {visibility: hidden;}
        # header {visibility: hidden;}
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

    with st.container():
        __, logo, title, __ = st.columns([2, 2, 6, 2])
        with logo:
            st.image(
                "assets/LOGO-UNRAM-1.png",
                width=150,
                use_column_width="never",
                caption="Universitas Mataram",
                output_format="auto",
            )
        with title:
            st.markdown(main_title, unsafe_allow_html=True)
            st.markdown(sub_title, unsafe_allow_html=True)
        st.markdown(
            '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
            unsafe_allow_html=True,
        )

    # SIDEBAR
    menu = st.sidebar.markdown(
        """
    <div style="display: flex; 
        justify-content: center;
        margin-bottom:-40px">
        <h3 style="text-align: center;">
        Pilih Menu</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )
    menu_option = st.sidebar.selectbox("", options=["Hitung TPM", "Managemen Pasien"])

    with st.sidebar.expander(
        label=":grey[Tutorial Penggunaan] :fast_forward: ",
        expanded=False,
    ):
        halaman = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Instruksi Penggunaan</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                        display: contents;
                        align-items: center;
                        justify-content: center;
                        # height: 100vh;
                    }

                    .instructions-container {
                        max-width: 100%;
                        # background-color: white;
                        padding: 2%;
                        border-radius: 20px;
                        box-shadow: 0 0 10px rgba(0, 1, 0, 0.5);
                        justify-content: center;
                        align-items: center;
                    }

                    .text-tutorial{
                        margin: 10px 0;
                        font-size: 15px;
                        line-height: 1.5;
                        color: white;
                    }

                    .important {
                        color: red;
                        # font-weight: bold;
                    }

                </>
            </head>
            <body>
                <div class="instructions-container">
                    <p class="text-tutorial" >1. Rekam video yang ingin diperiksa.</p>
                    <p class="text-tutorial">2. Unggah video ke situs web.</p>
                    <p style="text-align: center;"><img style="width: 250px; " src="https://archive.org/download/upload_202311/upload.png"/></p>
                    <p class="text-tutorial">3. Atur nilai kepercayaan.</p>
                    <p style="text-align: center;"><img style="width: 250px; " src="https://archive.org/download/confidence_202311/confidence.png"/></p>
                    <p class="text-tutorial">4. Atur line position.</p>
                    <p style="text-align: center;"><img style="width: 250px; " src="https://archive.org/download/lineposition/lineposition.png"/></p>
                    <p class="text-tutorial">5. Klik tombol Start.</p>
                    <p style="text-align: center;"><img style="width: 250px; " src="https://archive.org/download/start_20231122/start.png"/></p>
                    <p class="important">6. Jika posisi garis belum tepat, silakan diatur dan klik tombol Mulai kembali.</p>
                    <p class="text-tutorial">7. Hasil akan ditampilkan.</p>
                    <p style="text-align: center;"><img style="width: 50%; " src="https://archive.org/download/hasil_202311/hasil.png"/></p>
                </div>

            </body>
            </html>
            """
        st.markdown(
            halaman,
            unsafe_allow_html=True,
        )

    if menu_option == "Hitung TPM":
        st.sidebar.markdown(
            """
        <div style="display: flex; 
            justify-content: center;
            margin-bottom:-40px">
            <h3 style="text-align: center;">
            Upload a video</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        video_file_buffer = st.sidebar.file_uploader("", type=["mp4", "mov", "avi"])
        assigned_class_id = [0]
        names = ["tetesan"]
        st.sidebar.markdown(
            """
        <div style="display: flex; 
            justify-content: center;
            margin-bottom:-40px">
            <h3 style="text-align: center;">
            Confidence</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        confidence = st.sidebar.slider("", min_value=0.0, max_value=1.0, value=0.50)
        st.sidebar.markdown(
            """
        <div style="display: flex; 
            justify-content: center;
            margin-bottom:-40px">
            <h4 style="text-align: center;">
            Line position</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        lines = st.sidebar.number_input(
            "", min_value=0.00, max_value=1.00, value=0.461, step=0.001, format="%.3f"
        )

        st.markdown(
            '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
            unsafe_allow_html=True,
        )
        status = st.empty()
        tetesan, timer, fps = st.columns(3)
        # Result
        with tetesan:
            st.markdown(
                '<div style="text-align: center; margin-top: 20px"><font size="4" color="white">TETESAN</font></div>',
                unsafe_allow_html=True,
            )
            tetesan_text = st.markdown(line, unsafe_allow_html=True)

        with timer:
            st.markdown(
                '<div style="text-align: center; margin-top: 20px"><font size="4" color="white">TIMER</font></div>',
                unsafe_allow_html=True,
            )
            timer_text = st.markdown(line, unsafe_allow_html=True)

        with fps:
            st.markdown(
                '<div style="text-align: center; margin-top: 20px"><font size="4" color="white">FPS</font></div>',
                unsafe_allow_html=True,
            )
            fps_text = st.markdown(line, unsafe_allow_html=True)

        st.markdown(
            '<hr style="border: 1px solid #ffffff; margin: 20px 0;">',
            unsafe_allow_html=True,
        )

        col1, __, col2 = st.columns([2, 2, 2])
        with col1:
            if video_file_buffer:
                st.markdown(
                    '<p style="text-align:center;">Input Video</p>',
                    unsafe_allow_html=True,
                )
                st.video(video_file_buffer)

                # save video from streamlit into "videos" folder for future detect
                with open(os.path.join("videos", video_file_buffer.name), "wb") as f:
                    f.write(video_file_buffer.getbuffer())
        st.markdown(
            '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
            unsafe_allow_html=True,
        )

        if video_file_buffer is None:
            status.markdown(
                '<div style="text-align: center;"><font size="4" color="yellow"> Status: Waiting for input </font></div>',
                unsafe_allow_html=True,
            )
            st.toast("File berhasil dihapus")
        else:
            status.markdown(
                '<div style="text-align: center;"><font size= "4" color="green"> Status: Ready </font></div>',
                unsafe_allow_html=True,
            )
            st.toast("File berhasil diunggah")

        track_button = st.sidebar.button(
            "START", type="primary", use_container_width=True
        )
        stop_button = st.sidebar.button(
            "STOP", type="secondary", use_container_width=True
        )

        with col2:
            if track_button:
                st.toast("Proses dimulai!")
                if video_file_buffer is None:
                    status.markdown(
                        '<div style="text-align: center;"><font size= "4" color="red"> Status: Please! upload a video first </font></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<p style="text-align:center;">Output Video</p>',
                        unsafe_allow_html=True,
                    )
                    stframe = st.empty()
                    opt = parse_opt()
                    reset()
                    # opt.yolo_model = model_src
                    opt.conf_thres = confidence
                    opt.source = f"videos/{video_file_buffer.name}"

                    # Display the output video
                    output_video_path = os.path.join(
                        "inference", "output", video_file_buffer.name
                    )  # Update this path accordingly
                    if os.path.exists(output_video_path):
                        st.video(open(output_video_path, "rb").read())
                    status.markdown(
                        '<div style="text-align: center;"><font size="4" color="blue"> Status: Running </font></div>',
                        unsafe_allow_html=True,
                    )
                    with torch.no_grad():
                        detect(
                            opt,
                            stframe,
                            tetesan_text,
                            timer_text,
                            lines,
                            fps_text,
                            assigned_class_id,
                        )
                    status.markdown(
                        '<div style="text-align: center;"><font size="4" color="green"> Status: Finished! </font></div>',
                        unsafe_allow_html=True,
                    )
                    if stop_button:
                        st.stop()

    if menu_option == "Managemen Pasien":
        conn = sqlite3.connect("patient.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE if not exists patient_data (
                            nama_pasien varchar(50) not null,
                            id_pasien integer not null,
                            no_kamar varchar(10) not null,
                            tpm varchar(10) not null,
                            primary key(id_pasien)
                        );"""
        )

        def insert_patient_data(patient):
            if not is_no_kamar_unique(patient.room):
                raise ValueError(f"Nomor Kamar {patient.room} is already in use.")
            with conn:
                c.execute(
                    "insert into patient_data values (:name, :id, :room, :tpm)",
                    {
                        "name": patient.name,
                        "id": patient.id,
                        "room": patient.room,
                        "tpm": patient.tpm,
                    },
                )

        def is_no_kamar_unique(no_kamar):
            c.execute(
                "select count(*) from patient_data where no_kamar = :room",
                {"room": no_kamar},
            )
            count = c.fetchone()[0]
            return count == 0

        def get_patient_data_by_id(id_pasien):
            with conn:
                c.execute(
                    "select nama_pasien, id_pasien, no_kamar, tpm FROM patient_data where id_pasien = :id;",
                    {"id": id_pasien},
                )
                return c.fetchone()

        def remove_patient_data(id_pasien):
            with conn:
                c.execute(
                    "DELETE from patient_data WHERE id_pasien = :id", {"id": id_pasien}
                )

        def update_tpm(id_pasien, new_tpm):
            with conn:
                c.execute(
                    "update patient_data set tpm = :tpm where id_pasien = :id",
                    {"id": id_pasien, "tpm": new_tpm},
                )

        class Patient:
            def __init__(self, name, room, tpm):
                self.name = name
                self.id = None
                self.room = room
                self.tpm = tpm

        c.execute("select count(*) from patient_data")
        db_size = c.fetchone()[0]

        c.execute("select id_pasien from patient_data")
        id_pasiens = [i[0] for i in c.fetchall()]

        c.execute("SELECT * FROM patient_data")
        column_names = [col[0] for col in c.description]
        results = c.fetchall()
        df_results = pd.DataFrame(results, columns=column_names)
        st.markdown(
            """
        <div style="display: flex; 
            justify-content: center;
            margin-bottom: 10px">
            <h4 style="text-align: center;">
            Daftar Pasien</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.table(df_results)

        st.markdown("#####")
        if db_size >= 0:
            option = st.sidebar.selectbox("Pilih ID Pasien ", id_pasiens)
            with st.sidebar.expander(
                label=":grey[Tambah Pasien] ➕ ",
                expanded=False,
            ):
                nama_pasien = st.text_input("Nama Pasien ", "Rizaldy")
                no_kamar = st.text_input("Nomor Kamar ", "1")
                tpm = st.text_input("TPM", "20")
                st.markdown("####")
                if st.button("Simpan ⏬", use_container_width=True):
                    try:
                        patient = Patient(nama_pasien, no_kamar, tpm)
                        patient.id = db_size + 1
                        insert_patient_data(patient)
                        st.success(
                            f"Patient {nama_pasien}'s data is added to the Database!",
                            icon="✅",
                        )
                    except ValueError as e:
                        st.warning(f"Error: {e}", icon="⚠️")
                    except:
                        st.warning("Something went wrong! Try Again.", icon="⚠️")
                st.markdown("####")

        # Display column names
        c.execute("PRAGMA table_info(patient_data)")
        columns = c.fetchall()
        with st.sidebar.expander(
            label=":grey[Ubah TPM] ⚡️ ",
            expanded=False,
        ):
            new_tpm = st.text_input("TPM Baru", "20")
            if st.button("Ubah TPM ⚡️", use_container_width=True):
                try:
                    update_tpm(option, new_tpm)
                    st.success(f"{option}'s tpm is updated to {new_tpm}!", icon="✅")
                except:
                    st.info("Error updating patient tpm.", icon="ℹ️")
                else:
                    st.info("Database is Empty.", icon="ℹ️")

        with st.sidebar.expander(
            label=":grey[Hapus Pasien] ❌ ",
            expanded=False,
        ):
            if st.button("Hapus Pasien ❌", use_container_width=True):
                try:
                    remove_patient_data(option)
                    st.success(
                        f"Patient {option}'s data is removed from Database!",
                        icon="✅",
                    )
                except:
                    st.info("Error deleting patient data.", icon="ℹ️")
                else:
                    st.info("Database is Empty.", icon="ℹ️")

    # FOOTER
    footer_html = """
        <footer style="text-align: center; margin-top: 20px;">
            &copy; 2023 Andika Rizaldy. All rights reserved.
        </footer>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
