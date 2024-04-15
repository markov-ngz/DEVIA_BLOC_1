TEMP_TABLE_NAME = "temp_translation"
Q_CREATE_TABLE = f"""
            CREATE TABLE IF NOT EXISTS {TEMP_TABLE_NAME} (
                text_origin VARCHAR(1024),
                text_target VARCHAR(1024),
                extracted_at DATE,
                lang_origin VARCHAR(255),
                source_name VARCHAR(255),
                lang_target VARCHAR(255),
                source_type VARCHAR(255)
                )
            """

CREATE_TABLE_SOURCE  = """
    CREATE TABLE public.source
    (
        id serial,
        type character varying(256),
        name character varying(1024),
        PRIMARY KEY (id)
    )
"""
CREATE_TABLE_LANGUAGE = """
CREATE TABLE public.languages
(
    id serial,
    lang_origin character varying(256),
    lang_target character varying(1024),
    PRIMARY KEY (id)
)   
"""

CREATE_TABLE_TRANSLATIONS = """
    CREATE  TABLE public.translations
    (
        id serial,
        text_origin character varying(1024),
        text_target character varying(1024),
        extracted_at date,
        languages_id integer,
        source_id integer,
        PRIMARY KEY (id),
        CONSTRAINT source_id FOREIGN KEY (source_id)
            REFERENCES public.source (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID,
        CONSTRAINT languages_id FOREIGN KEY (languages_id)
            REFERENCES public.languages (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
    )
    """

CREATE_VIEW = """
    CREATE OR REPLACE VIEW translation_view
    AS
    SELECT DISTINCT
        l.lang_origin,
        l.lang_target,
        text_origin,
        text_target,
        extracted_at,
        s.type as source_type,
        s.name as source_name
    FROM translations t
    LEFT JOIN source s ON s.id = t.source_id
    LEFT JOIN languages l ON l.id = t.languages_id
"""

INSERT_LANGUAGES = f"""
    INSERT INTO languages(lang_origin , lang_target)
    SELECT DISTINCT 
        lang_origin , 
        lang_target
    FROM {TEMP_TABLE_NAME}
    """

INSERT_SOURCE = f"""
    INSERT INTO source(type , name)
    SELECT DISTINCT 
        source_name , 
        source_type
    FROM  {TEMP_TABLE_NAME}
"""

INSERT_TRANSLATIONS = f"""
    WITH trans AS (
        SELECT
            text_origin,
            text_target,
            extracted_at,
            l.id as languages_id,
            s.id as source_id
        FROM  {TEMP_TABLE_NAME} t
        LEFT JOIN languages l on l.lang_origin = t.lang_origin and l.lang_target = t.lang_target
        LEFT JOIN source s on s.type = t.source_name and s.name = t.source_type
    )
    INSERT INTO translations (text_origin, text_target,extracted_at, languages_id, source_id)
    SELECT * FROM trans
    """



DELETE_TEMP = f"""DELETE FROM {TEMP_TABLE_NAME}"""