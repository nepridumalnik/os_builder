set(TARGET boot)

set(SOURCES
    assembler/boot.s
)

set(CMAKE_EXE_LINKER_FLAGS
    "-m elf_i386 -T ${CMAKE_CURRENT_SOURCE_DIR}/assembler/linker.ld"
)

set_property(SOURCE ${SOURCES} APPEND PROPERTY COMPILE_OPTIONS "-32")

add_executable(${TARGET} ${SOURCES})
