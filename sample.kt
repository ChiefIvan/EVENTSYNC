fun main() {
    val numbers: List<Int> = listOf(1, 2, 3, 4, 5)
    val positives = numbers.filter({ number: Int -> number % 2 != 0 })
    print(positives)
}