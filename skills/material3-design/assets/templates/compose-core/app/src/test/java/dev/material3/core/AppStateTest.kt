package dev.material3.core

import org.junit.Assert.assertEquals
import org.junit.Test

class AppStateTest {
    @Test
    fun selection_changes_without_changing_destination_identity() {
        assertEquals(
            Destination.Settings,
            selectedDestination(Destination.Home, Destination.Settings),
        )
    }

    @Test
    fun reduced_motion_removes_ornamental_duration() {
        assertEquals(0, AppMotion.duration(AppMotion.EmphasizedMillis, reducedMotion = true))
        assertEquals(180, AppMotion.duration(AppMotion.StandardMillis, reducedMotion = false))
    }
}
