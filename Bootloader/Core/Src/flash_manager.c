
#include <stdio.h>
#include "stm32f4xx_hal.h"

#include "flash_manager.h"
#include "config.h"



void erase_application_flash(void)
{
    HAL_FLASH_Unlock();

    FLASH_EraseInitTypeDef eraseInitStruct;
    uint32_t sectorError;

    eraseInitStruct.TypeErase    = FLASH_TYPEERASE_SECTORS;
    eraseInitStruct.VoltageRange = FLASH_VOLTAGE_RANGE_3;
    eraseInitStruct.Sector       = FLASH_SECTOR_4;
    eraseInitStruct.NbSectors    = 4;   // 4,5,6,7

    if (HAL_FLASHEx_Erase(&eraseInitStruct, &sectorError) != HAL_OK)
    {
        // Optional: send error over UART
    }

    HAL_FLASH_Lock();
}
