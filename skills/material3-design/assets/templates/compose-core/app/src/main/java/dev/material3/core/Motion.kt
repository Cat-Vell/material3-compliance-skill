package dev.material3.core

object AppMotion {
    const val StandardMillis = 180
    const val EmphasizedMillis = 300

    fun duration(millis: Int, reducedMotion: Boolean): Int =
        if (reducedMotion) 0 else millis
}
