TEMPLATE = app
CONFIG += console c++17
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
        encuesta.cpp \
        main.cpp \
        pregunta.cpp \
        respuestas.cpp \
        sistemaencuesta.cpp

HEADERS += \
    encuesta.h \
    pregunta.h \
    respuestas.h \
    sistemaencuesta.h
