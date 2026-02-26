#include "jump.h"
extern UART_HandleTypeDef huart3;

#include "config.h"

void go_to_function(void){


	void(*app_reset_handler)(void) = (void*)(*(volatile uint32_t *)(0x08010000 + 4));
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);


	app_reset_handler();

}


uint8_t is_application_valid(void)
{
    uint32_t app_stack = *(volatile uint32_t*)APP_START_ADDRESS;
    uint32_t valid_flag = *(volatile uint32_t*)APP_FLAG_ADDRESS;

    if ((app_stack >= SRAM_START) && (app_stack <= SRAM_END) && (valid_flag == APP_VALID_FLAG))
    {
        return 1;
    }

    return 0;
}
